"""
Exception handlers
"""

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request, status
from app.models.responses import APIResponse, ErrorDetail
from app.core.constants import ErrorCode

async def global_exception_handler(request: Request, exc: Exception):
    """
    Handle all unexpected exceptions globally while retaining API documentation.
    """
    # NOTE :: log the exception here

    response_data = APIResponse[None](
        success=False,
        message="An unexpected error occurred.",
        data=None,
        error=ErrorDetail(code=ErrorCode.SERVER_ERROR)
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response_data.model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors.
    """
    # NOTE :: log the validation error here

    validation_errors = {}
    for error in exc.errors():
        field = ".".join(map(str, error["loc"]))
        validation_errors[field] = error["msg"]

    response_data = APIResponse[None](
        success=False,
        message="Validation failed.",
        data=None,
        error=ErrorDetail(code=ErrorCode.VALIDATION_ERROR, details=validation_errors)
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_data.model_dump()
    )
