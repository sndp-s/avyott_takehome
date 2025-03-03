"""
Authors services
"""


from app.db.queries import authors as authors_queries
from app.models import authors as authors_models


def get_all_authors_service(db, offset=0, limit=10):
    """
    Fetch all authors with optional filters and pagination.
    """
    all_authors = authors_queries.get_all_authors_query(db, offset, limit)
    return all_authors


def get_author_service(db, author_id):
    """
    Returns the authors matching the given author_id
    """
    author = authors_queries.get_author(db, author_id)
    return author


def add_new_author_service(db, book: authors_models.AuthorCreate) -> authors_models.Author:
    """
    Add a new Author to the library database
    """
    author_id = authors_queries.add_new_author_query(db, book)
    return author_id
