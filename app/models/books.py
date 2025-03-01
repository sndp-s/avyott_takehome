"""
Pydantic models for Books API request response validation
"""

from datetime import date
from pydantic import BaseModel
from pydantic_extra_types.isbn import ISBN


# Request
class BaseBook(BaseModel):
    """
    Base model for the Books entity
    """
    title: str
    isbn: ISBN
    genre: str
    publication_date: date
    available_copies: int = 0


class BookCreate(BaseBook):
    """
    Model for 'Create new Book' entity request
    """
    author_ids: list[int]


class Book(BaseBook):
    """
    Books entity model
    """
    id: int


class BookUpdate(BaseModel):
    """
    Model for Book entity udpate requests
    """
    title: str | None = None
    isbn: ISBN | None = None
    genre: str | None = None
    publication_date: date | None = None
    available_copies: int | None = None
    author_ids: list[int] | None = None


# Response
class BookAuthor(BaseModel):
    """
    Model of Author entity as found in the Books response
    """
    id: int
    first_name: str
    last_name: str


# TODO :: refactor it to BookWithAuthors
class BookResponse(Book):
    """
    Book response model
    """
    authors: list[BookAuthor]
