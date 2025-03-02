"""
Exception handlers
"""

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
