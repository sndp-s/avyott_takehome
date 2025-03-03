"""
Author models.
"""
from datetime import date
from pydantic import BaseModel


class BaseAuthor(BaseModel):
    """
    Base model for Author entity.
    """
    first_name: str
    last_name: str
    date_of_birth: date


class Author(BaseAuthor):
    """
    Author entity model.
    """
    id: int


class AuthorCreate(BaseAuthor):
    """
    Model for 'create author' API request body.
    """
    date_of_birth: date | None = None
