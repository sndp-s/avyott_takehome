"""
Books services
"""

from app.db.queries import books as books_queries
from app.models import books as books_models


def get_all_books_service(db, filters=None, offset=0, limit=10):
    """
    Fetch all books with optional filters and pagination.
    """
    # TODO :: Implement error handling
    all_books = books_queries.get_all_books_query(db, filters, offset, limit)
    return all_books


def get_book_service(db, book_id):
    """
    Returns the books matching the given book_id
    """
    # TODO :: Implement error handling
    book = books_queries.get_book(db, book_id)
    return book


def add_new_book_service(db, book: books_models.BookCreate):
    """
    Add a new book to the library database
    """
    added_book = books_queries.add_new_book(db, book)
    return added_book
