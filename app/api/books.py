"""
Books APIs router
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path
from app.db.connection import get_db
from app.services import books as books_service
from app.models import books as books_models

router = APIRouter()

@router.get("")
async def get_all_books(
    db=Depends(get_db),
    # TODO :: Accept a filters parameter,
    # TODO :: Fix error on absence of optional query params
    offset: int = Annotated[int, Query(0, ge=0, description="Starting index")],
    limit: int = Annotated[int, Query(10, ge=1, le=100, description="Number of items to retrieve")]
) -> list[books_models.BookResponse]:
    """
    Returns all the books in the library with their basic info.
    """
    all_books = books_service.get_all_books_service(db, {}, offset, limit)
    return all_books


@router.get("/{book_id}")
async def get_book(
    book_id: Annotated[int, Path()],
    db=Depends(get_db)
) -> books_models.BookResponse:
    """
    Returns the books corresponding to the given book_id
    """
    book = books_service.get_book_service(db, book_id)
    return book


@router.post("")
async def create_book(
    book: books_models.BookCreate,
    db=Depends(get_db)
) -> int:
    """
    Adds a new book to the library.
    """
    added_book = books_service.add_new_book_service(db, book)
    return added_book
