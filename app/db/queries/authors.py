"""
Query wrappers for Authors entity.
"""


import psycopg2
from app.db.helpers import \
    execute_sql_fetch_all, execute_sql_fetch_one
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


def get_author(db, author_id):
    """
    Fetch the Author matching the given author_id.
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
        Where id = %(author_id)s;
        """
        params = {'author_id': author_id}
        author = execute_sql_fetch_one(db, sql, params)
        if not author:
            raise custom_exceptions.RecordNotFoundException("Author not found")
        return author
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to fetch the Author."
        )
