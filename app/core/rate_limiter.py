from typing import cast

from fastapi import Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.config import settings


def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
    return _rate_limit_exceeded_handler(request, cast(RateLimitExceeded, exc))


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        f"{settings.RATELIMIT_SECOND}/second",
        f"{settings.RATELIMIT_MINUTE}/minute",
        f"{settings.RATELIMIT_HOUR}/hour",
        f"{settings.RATELIMIT_DAY}/day",
    ],
)
