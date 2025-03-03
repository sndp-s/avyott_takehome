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


def get_patron_service(db, patron_id):
    """
    Returns the patron matching the given patron_id
    """
    patron = patrons_queries.get_patron_query(db, patron_id)
    return patron
