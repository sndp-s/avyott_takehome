"""
Query wrappers for Authors entity.
"""


import psycopg2
from app.db.helpers import \
    execute_sql_fetch_all, execute_sql_fetch_one
from app.core import exceptions as custom_exceptions
from app.models import authors as authors_models

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


def add_new_author_query(db, author) -> authors_models.Author:
    """
    Add a new author record to the database.
    """
    try:
        params = {
            'first_name': author.first_name,
            'last_name': author.last_name,
            'date_of_birth': author.date_of_birth
        }

        sql = """
        INSERT INTO authors (first_name, last_name, date_of_birth)
        VALUES (%(first_name)s, %(last_name)s, %(date_of_birth)s)
        RETURNING id, first_name, last_name, date_of_birth;
        """

        with db.cursor() as cursor:
            cursor.execute(sql, params)
            author_id, first_name, last_name, date_of_birth = cursor.fetchone()
            db.commit()

            return authors_models.Author(
                id=author_id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth
            )

    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to add author to the library."
        )


def update_author_query(db, author_id, update_data):
    """
    Update an existing author in the database.
    """
    try:
        with db.cursor() as cursor:
            # Prepare the UPDATE statement
            set_clauses = []
            params = {"author_id": author_id}

            for key, value in update_data.items():
                set_clauses.append(f"{key} = %({key})s")
                params[key] = value

            author_updated = None
            if set_clauses:
                sql = f"""
                UPDATE authors
                SET {', '.join(set_clauses)}
                WHERE id = %(author_id)s
                RETURNING id, first_name, last_name, date_of_birth;
                """
                cursor.execute(sql, params)
                author_updated = cursor.fetchone()

            if not author_updated:
                raise custom_exceptions.RecordNotFoundException("The author with the given ID does not exist.")

        db.commit()
        return authors_models.Author(
            id=author_updated[0],
            first_name=author_updated[1],
            last_name=author_updated[2],
            date_of_birth = author_updated[3]
        )
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to update the author."
        )
