# Standard Libraries
from functools import wraps

# Third-party Libraries
import structlog
from asgiref.sync import sync_to_async
from django.db import close_old_connections, utils

logger = structlog.getLogger(__name__)


def async_database():
    def decorator(func):
        @sync_to_async(thread_sensitive=True)
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (utils.InterfaceError, utils.OperationalError):
                close_old_connections()
                logger.info("async_database: close_old_connections()")
                return func(*args, **kwargs)

        return wrapper

    return decorator
