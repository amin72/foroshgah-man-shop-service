import uuid
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_structlog.middleware import StructlogMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from tortoise.backends.base.config_generator import generate_config
from tortoise.contrib.fastapi import RegisterTortoise

from app.api.v1.endpoints import shop as shop_v1
from app.api.v1.endpoints import category as category_v1
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.core.rate_limiter import limiter, rate_limit_exceeded_handler

configure_logging()


app_v1 = FastAPI(
    title=f"{settings.PROJECT_NAME} V1",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    generate_unique_id_function=lambda route: f"v1-{route.name}",
)


# Include versioned routers
app_v1.include_router(shop_v1.router, prefix="/shop", tags=["shop"])
app_v1.include_router(category_v1.router, prefix="/category", tags=["category"])


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Database setup
    config = generate_config(
        settings.database_url,
        app_modules={"models": ["app.models"]},
        connection_label="models",
    )
    async with RegisterTortoise(
        app=app,
        config=config,
        generate_schemas=False,
        add_exception_handlers=True,
    ):
        # Database is connected
        yield
        # Application teardown
    # Database connections are closed


# Create a master FastAPI app that mounts the versioned apps
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


limiter.enabled = settings.RATELIMIT_ENABLED

app_v1.state.limiter = limiter

app_v1.add_middleware(SlowAPIMiddleware)

app_v1.add_exception_handler(
    RateLimitExceeded,
    rate_limit_exceeded_handler,
)

if settings.BACKEND_CORS_ORIGINS:
    app_v1.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Mount the versioned apps
app.mount("/v1", app_v1)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def main_docs() -> HTMLResponse:
    return HTMLResponse(content=open("static/index.html").read())


app.add_middleware(StructlogMiddleware)


@app.middleware("http")
async def logging_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Any]]
) -> Response:
    # Generate a unique request ID if not provided
    req_id = request.headers.get("request-id", str(uuid.uuid4()))

    # Bind initial context
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=req_id,
        method=request.method,
        url=str(request.url),
    )

    try:
        # Process the request
        response: Response = await call_next(request)

        # Add response status code to the context
        structlog.contextvars.bind_contextvars(status_code=response.status_code)

        return response

    except HTTPException as exc:
        # Handle HTTP exceptions
        structlog.contextvars.bind_contextvars(status_code=exc.status_code)
        structlog.get_logger().error("HTTPException occurred", exc_info=True)
        raise exc

    except Exception as exc:
        # Handle all other exceptions
        structlog.get_logger().error("Unexpected error occurred", exc_info=True)
        raise exc
