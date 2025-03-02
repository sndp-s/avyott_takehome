"""
Constants across the app
"""

from enum import Enum


class ErrorCode(str, Enum):
    """
    Standard error codes
    """
    SERVER_ERROR = "server_error"
    VALIDATION_ERROR = "validation_error"
    BAD_REQUEST = "bad_request"
    INTEGRITY_ERROR = "integrity_error"
    DATABASE_ERROR = "database_error"
    NOT_FOUND = "not_found"

