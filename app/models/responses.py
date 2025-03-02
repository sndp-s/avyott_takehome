"""
Response model
"""

from typing import Generic, TypeVar, Any
from pydantic import BaseModel
from app.core.constants import ErrorCode

T = TypeVar("T")

class ErrorDetail(BaseModel):
    """
    ErrorDetail model
    """
    code: ErrorCode
    details: dict[str, Any] | None = None


class APIResponse(BaseModel, Generic[T]):
    """
    Generic API response structure
    """
    success: bool = True
    message: str
    data: T | None = None
    error: ErrorDetail
