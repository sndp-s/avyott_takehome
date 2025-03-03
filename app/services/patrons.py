"""
Patrons services
"""

from app.db.queries import patrons as patrons_queries
from app.models import patrons as patrons_models


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


def add_new_patron_service(db, patron: patrons_models.PatronCreate) -> patrons_models.Patron:
    """
    Add a new Patron to the library database.
    """
    patron = patrons_queries.add_new_patron_query(db, patron)
    return patron


def update_patron_service(db, patron_id: int, update_data: dict) -> patrons_models.Patron:
    """
    Update a patron record.
    """
    updated_patron = patrons_queries.update_patron_query(db, patron_id, update_data)
    return updated_patron
