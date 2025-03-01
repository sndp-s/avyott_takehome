"""
Helper functions for database operations
"""

import psycopg2
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
        raise HTTPException(status_code=500, detail="Database error")


def execute_sql_fetch_all(db, sql, params=None):
    """Executes a SQL query and returns all results as a list of dictionaries."""
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            return fetchall_dict(cursor)
    except psycopg2.Error as e:
        # TODO :: log error here
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")


def execute_sql_update(db, sql, params=None):
    """Execute an update (INSERT, DELETE, UPDATE) SQL statement and commit/rollback transaction"""
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, params)
            db.commit()
            return cursor.rowcount  # number of rows affected
    except psycopg2.Error as e:
        # TODO :: log error here
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
