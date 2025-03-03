"""
Query wrappers for Authors entity.
"""


import psycopg2
from app.db.helpers import \
    execute_sql_fetch_all
from app.core import exceptions as custom_exceptions


def get_all_authors_query(db, offset, limit):
    """
    Return all Authors.
    """
    try:
        sql = \
        """
        SELECT
            id,
            first_name,
            last_name,
            date_of_birth
        FROM
            Authors
        OFFSET %(offset)s LIMIT %(limit)s;
        """
        params = {'offset': offset, 'limit': limit}
        all_authors = execute_sql_fetch_all(db, sql, params)
        return all_authors
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to fetch authors."
        )
