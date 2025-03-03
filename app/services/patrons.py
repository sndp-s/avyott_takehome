"""
Patrons services
"""

from app.db.queries import patrons as patrons_queries


def get_all_patrons_service(db, offset=0, limit=10):
    """
    Fetch all patrons.
    """
    all_patrons = patrons_queries.get_all_patrons_query(db, offset, limit)
    return all_patrons
