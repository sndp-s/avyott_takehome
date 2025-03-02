"""
Response model
"""

from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """
    Generic API response structure
    """
    success: bool = True
    message: str
    data: T | None = None
