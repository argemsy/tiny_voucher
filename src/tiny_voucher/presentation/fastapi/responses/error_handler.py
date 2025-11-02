# Standard Libraries
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar

# Third-party Libraries
import structlog
from fastapi.responses import JSONResponse

# Own Libraries
from src.tiny_voucher.presentation.fastapi.responses.errors import ErrorSchema
from src.tiny_voucher.shared.enums import ErrorSchemaEnum
from src.tiny_voucher.shared.exceptions import DomainExceptionError
from src.tiny_voucher.shared.utils.generator_operation_identifier import (
    get_operation_id,
)

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def error_response_handler(path: str) -> Callable[[F], F]:
    """Decorator to handle domain and internal exceptions in FastAPI
    endpoints.

    Args:
        path (str): Module or router path used for logging context.

    Returns:
        Callable[[F], F]: Wrapped async function returning JSONResponse
        on error.

    Wraps an async FastAPI route handler, automatically capturing
    `DomainExceptionError` and general `Exception`. Returns standardized
    JSONResponse objects with error metadata and operation ID.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            log_tag = func.__name__
            logger = structlog.getLogger(path)
            operation_id = get_operation_id()
            logger.debug(f"***{log_tag} Start")
            try:
                return await func(*args, **kwargs)
            except DomainExceptionError as exp:
                logger.error(f"***{log_tag}*** ValidationError. {str(exp)}")
                return JSONResponse(
                    status_code=400,
                    content=ErrorSchema(
                        operation_id=operation_id,
                        type=ErrorSchemaEnum.VALIDATION_ERROR,
                        message=str(exp),
                    ).dict(),
                )
            except Exception as exp:
                logger.error(f"***{log_tag}*** InternalError. {exp!r}")
                return JSONResponse(
                    status_code=500,
                    content=ErrorSchema(
                        operation_id=operation_id,
                        type=ErrorSchemaEnum.INTERNAL_ERROR,
                        message="InternalError",
                    ).dict(),
                )

        return wrapper  # type: ignore

    return decorator
