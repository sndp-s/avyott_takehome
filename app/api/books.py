"""
Books APIs router
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query
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
