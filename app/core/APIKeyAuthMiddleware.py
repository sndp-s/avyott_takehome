"""
API Key based Authentication middleware
"""

from fastapi.responses import JSONResponse
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.constants import ErrorCode
from app.models.responses import APIResponse, ErrorDetail


class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    """
    Authenticates requests by matching its API key
    """
    async def dispatch(self, request: Request, call_next):
        # Let the documentation endpoints bypass authentication
        if request.url.path in ["/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)

        # Authenticate the request
        api_key = request.headers.get('X-API-KEY')
        if api_key is None or api_key != settings.api_key:
            response_data = APIResponse[None](
                success=False,
                message="Invalid or missing API Key",
                data=None,
                error=ErrorDetail(code=ErrorCode.UNAUTHORIZED)
            )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=response_data.model_dump()
            )
        return await call_next(request)
