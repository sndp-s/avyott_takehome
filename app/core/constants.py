"""
Constants across the app
"""

from enum import Enum


class ErrorCode(str, Enum):
    """
    Standard error codes
    """
    SERVER_ERROR = "server_error"
