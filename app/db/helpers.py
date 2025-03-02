"""
Helper functions for database operations
"""

import psycopg2
from psycopg2.extras import execute_values
from fastapi import HTTPException


def fetchall_dict(cursor):
    """Return all rows from a cursor as a list of dictionaries."""
    columns = [col.name for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def execute_sql_fetch_one(db, sql, params=None):
    """Executes a SQL query and returns a single result as a dictionary."""
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            if result:
                return dict(zip([col.name for col in cursor.description], result))
            else:
                return None
    except psycopg2.Error as e:
        # TODO :: log error here
        db.rollback()
        raise


def execute_sql_fetch_all(db, sql, params=None):
    """Executes a SQL query and returns all results as a list of dictionaries."""
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            return fetchall_dict(cursor)
    except psycopg2.Error as e:
        # TODO :: log error here
        db.rollback()
        raise


def execute_sql_update(db, sql, params=None):
    """Execute an update (INSERT, DELETE, UPDATE) SQL statement and commit/rollback transaction"""
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            db.commit()
            return cursor.rowcount  # number of rows affected
    except psycopg2.Error as e:
        # TODO :: add log here
        db.rollback()
        raise


def execute_sql(
    db,
    sql,
    params=None,
    *,
    returning: bool = False,
    fetch_all: bool = False,
    bulk: bool = False
):
    """
    Execute a SQL statement.

    Parameters:
      - db: The database connection.
      - sql: The SQL query.
      - params: Optional parameters for the query.
      - returning: If True, fetch returned rows.
      - fetch_all: If True and returning is True, fetch all rows; otherwise, fetch one row.
      - bulk: If True, perform a bulk operation. In this case, 'params' should be a list of tuples.

    Returns:
      - If returning is False: the rowcount (number of rows affected).
      - If returning is True: the fetched result(s).
    """
    try:
        with db.cursor() as cursor:
            if bulk:
                # For bulk operations, params should be a list of tuples
                execute_values(cursor, sql, params)
            else:
                cursor.execute(sql, params)

            if returning:
                result = cursor.fetchall() if fetch_all else cursor.fetchone()
            else:
                result = cursor.rowcount

            db.commit()
            return result

    except psycopg2.Error as e:
        # TODO :: add log here
        db.rollback()
        raise
