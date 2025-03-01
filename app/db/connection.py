"""
Database utils
"""

import psycopg2
from psycopg2.pool import SimpleConnectionPool
from fastapi import HTTPException
from app.core.config import settings

db_pool = None


def get_db_pool():
    """
    DB pool getter
    """
    global db_pool
    if db_pool is None:
        try:
            db_pool = SimpleConnectionPool(
                minconn=settings.minconn,
                maxconn=settings.maxconn,
                host=settings.db_host,
                database=settings.db_name,
                user=settings.db_user,
                password=settings.db_password,
                port=settings.db_port
            )
        except psycopg2.OperationalError as e:
            # TODO :: log error here
            raise HTTPException(
                status_code=500, detail="Database connection error")
    return db_pool


def get_db():
    """
    DB connection getter
    """
    pool = get_db_pool()
    conn = pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)
