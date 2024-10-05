import logging
from collections.abc import Mapping, MutableMapping
from logging.handlers import RotatingFileHandler
from typing import Any, cast

import structlog


def _extract_from_record(
    _: Any, __: Any, event_dict: MutableMapping[str, Any]
) -> Mapping[str, Any]:
    """Extract thread and process names and add them to the event dict."""
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName
    return event_dict


def _configure_default_logging_by_custom(
    shared_processors: list[structlog.types.Processor],
    logs_render: structlog.types.Processor,
) -> None:
    """Configure logging handlers and formatters."""
    logging.getLogger("watchfiles").setLevel(logging.WARNING)

    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=500 * 1024 * 1024, backupCount=3
    )

    # Use `ProcessorFormatter` to format all `logging` entries.
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            _extract_from_record,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            logs_render,
        ],
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)

    root_uvicorn_logger = logging.getLogger()
    root_uvicorn_logger.setLevel(logging.INFO)
    root_uvicorn_logger.addHandler(console_handler)
    root_uvicorn_logger.addHandler(file_handler)


def configure_logging(enable_json_logs: bool = False) -> None:
    """Configure logging for the application."""
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors: list[structlog.types.Processor] = [
        timestamper,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.contextvars.merge_contextvars,
        structlog.processors.CallsiteParameterAdder({
            structlog.processors.CallsiteParameter.PATHNAME,
            structlog.processors.CallsiteParameter.FILENAME,
            structlog.processors.CallsiteParameter.MODULE,
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.THREAD,
            structlog.processors.CallsiteParameter.THREAD_NAME,
            structlog.processors.CallsiteParameter.PROCESS,
            structlog.processors.CallsiteParameter.PROCESS_NAME,
        }),
        structlog.stdlib.ExtraAdder(),
    ]

    structlog.configure(
        processors=shared_processors
        + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )

    logs_render: structlog.types.Processor = cast(
        structlog.types.Processor,
        structlog.processors.JSONRenderer()
        if enable_json_logs
        else structlog.dev.ConsoleRenderer(colors=True),
    )

    _configure_default_logging_by_custom(shared_processors, logs_render)
