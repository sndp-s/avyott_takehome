"""
Books APIs router
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path
from app.db.connection import get_db
from app.services import books as books_service
from app.models import books as books_models
from app.models.responses import APIResponse

router = APIRouter()

@router.get("")
async def get_all_books(
    db=Depends(get_db),
    filters: books_models.BookFilters = Depends(),
    offset: Annotated[int, Query(ge=0, description="Starting index")]=0,
    limit: Annotated[int, Query(ge=1, le=100, description="Number of items to retrieve")]=10
) -> APIResponse[list[books_models.Book]]:
    """
    Returns all the books in the library with their basic info.
    """
    all_books = books_service.get_all_books_service(db, filters, offset, limit)
    return APIResponse(
        data=all_books,
        message="Books fetched successfully"
    )


@router.get("/{book_id}")
async def get_book(
    book_id: Annotated[int, Path()],
    db=Depends(get_db)
) -> APIResponse[books_models.Book]:
    """
    Returns the books corresponding to the given book_id
    """
    book = books_service.get_book_service(db, book_id)
    return APIResponse(
        data=book,
        message='Book fetched successfully'
    )


@router.post("")
async def create_book(
    book: books_models.BookCreate,
    db=Depends(get_db)
) -> APIResponse[int]:
    """
    Adds a new book to the library.
    """
    added_book = books_service.add_new_book_service(db, book)
    return APIResponse(
        data=added_book,
        message="Book added successfully"
    )


@router.put("/{book_id}")
async def update_book(
    book_id: Annotated[int, Path()],
    book: books_models.BookUpdate,
    db=Depends(get_db)
) -> APIResponse[int]:
    """
    Update an existing book.
    """
    book_id = books_service.update_book_service(db, book_id, book.dict(exclude_unset=True))
    return APIResponse(
        data=book_id,
        message="Book updated successfully"
    )


@router.delete("/{book_id}")
async def delete_book(
    book_id: Annotated[int, Path()],
    db=Depends(get_db)
) -> APIResponse[bool]:
    """
    Deletes the book corresponsing to given book_id.
    """
    books_service.delete_book_service(db, book_id)
    return APIResponse(message="Book deleted")


# TODO :: Implement books search API
