"""
Authors services
"""

from app.db.queries import authors as authors_queries


def get_all_authors_service(db, offset=0, limit=10):
    """
    Fetch all authors with optional filters and pagination.
    """
    all_authors = authors_queries.get_all_authors_query(db, offset, limit)
    return all_authors
