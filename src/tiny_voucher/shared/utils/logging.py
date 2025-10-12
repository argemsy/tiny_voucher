# Standard Libraries
import logging
from typing import Any, Callable, Mapping, MutableMapping

# Third-party Libraries
import structlog


def configure_structlog(debug: bool = False) -> None:
    """Configures structlog and standard logging for the application.

    Sets up log processors, formatting, and log levels for both structlog
    and the standard logging module. Switches between console and JSON
    output based on the debug flag.

    Args:
        debug (bool): If True, enables console renderer with colors;
        otherwise uses JSON renderer.

    Returns:
        None
    """
    shared_processors: list[
        Callable[[Any, str, MutableMapping[str, Any]], Mapping[str, Any]]
    ] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    renderer = (
        structlog.dev.ConsoleRenderer(colors=True)
        if debug
        else structlog.processors.JSONRenderer()
    )

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.processors.EventRenamer("message"),
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler()],
    )

    logging.getLogger("django").setLevel(logging.INFO)
    logging.getLogger("django.server").setLevel(logging.INFO)
