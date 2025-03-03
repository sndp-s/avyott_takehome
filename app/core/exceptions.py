"""
Application exceptions
"""

from fastapi import HTTPException, status


class CustomAPIException(HTTPException):
    """
    Base custom API exception.
    """
    def __init__(self, detail: str, status_code: int):
        super().__init__(status_code=status_code, detail=detail)


class DuplicateEntryException(CustomAPIException):
    """
    Raised when a record with the given unique identifier already exists.
    """
    def __init__(self, detail: str = "Record already exists."):
        super().__init__(detail, status.HTTP_409_CONFLICT)


class ForeignKeyNotFoundException(CustomAPIException):
    """
    Raised when referenced foreign key does not exist.
    """
    def __init__(self, detail: str = "The related item could not be found."):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class DatabaseOperationException(CustomAPIException):
    """
    Raised for all other database exceptions.
    """
    def __init__(self, detail: str = ""):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoanPendingException(CustomAPIException):
    """
    Raised when an entity with pending loans is attempted to be deleted.
    """
    def __init__(self, detail: str = "Operation cannot be completed; there are pending loans."):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class RecordNotFoundException(CustomAPIException):
    """
    Raised when requested record not found.
    """
    def __init__(self, detail: str = "Record not found"):
        super().__init__(detail, status.HTTP_404_NOT_FOUND)
