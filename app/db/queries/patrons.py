"""
Query wrappers for Authors entity.
"""


import psycopg2
from app.db.helpers import execute_sql_fetch_all
from app.core import exceptions as custom_exceptions
from app.models import patrons as patrons_models


def get_all_patrons_query(db, offset, limit):
    """
    Return all Patrons.
    """
    try:
        sql = \
        """
        SELECT
            id,
            first_name,
            last_name,
            email,
            registration_date
        FROM
            patrons
        OFFSET %(offset)s LIMIT %(limit)s;
        """
        params = {'offset': offset, 'limit': limit}
        all_patrons = execute_sql_fetch_all(db, sql, params)
        return all_patrons
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to fetch Patrons."
        )
