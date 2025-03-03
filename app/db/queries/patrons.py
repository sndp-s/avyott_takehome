"""
Query wrappers for Authors entity.
"""


import psycopg2
from app.db.helpers import \
    execute_sql_fetch_all, execute_sql_fetch_one
from app.core import exceptions as custom_exceptions
from app.models import patrons as patrons_models
from datetime import date


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


def get_patron_query(db, patron_id):
    """
    Fetch the Patron matching the given patron_id.
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
        Where id = %(patron_id)s;
        """
        params = {'patron_id': patron_id}
        patron = execute_sql_fetch_one(db, sql, params)
        if not patron:
            raise custom_exceptions.RecordNotFoundException("Patron not found")
        return patron
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to fetch the Patron."
        )


def add_new_patron_query(db, patron) -> patrons_models.Patron:
    """
    Add a new patron record to the database.
    """
    try:
        params = {
            'first_name': patron.first_name,
            'last_name': patron.last_name,
            'email': patron.email,
            'registration_date': date.today()
        }

        sql = """
        INSERT INTO patrons (first_name, last_name, email, registration_date)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(registration_date)s)
        RETURNING id, first_name, last_name, email, registration_date;
        """

        with db.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()

        db.commit()

        patron_id, first_name, last_name, email, registration_date = result

        return patrons_models.Patron(
            id=patron_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            registration_date=registration_date
        )
    except psycopg2.errors.UniqueViolation as e:
        db.rollback()
        raise custom_exceptions.DuplicateEntryException(
            "The given Email ID is already registered in the system."
        )
    except psycopg2.Error:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to register patron to the library."
        )


def update_patron_query(db, patron_id, update_data):
    """
    Update an existing patron in the database.
    """
    try:
        with db.cursor() as cursor:
            # Prepare the UPDATE statement
            set_clauses = []
            params = {"patron_id": patron_id}

            for key, value in update_data.items():
                set_clauses.append(f"{key} = %({key})s")
                params[key] = value

            patron_updated = None
            if set_clauses:
                sql = f"""
                UPDATE patrons
                SET {', '.join(set_clauses)}
                WHERE id = %(patron_id)s
                RETURNING id, first_name, last_name, email, registration_date;
                """
                cursor.execute(sql, params)
                patron_updated = cursor.fetchone()

            if not patron_updated:
                raise custom_exceptions.RecordNotFoundException("The patron with the given ID does not exist.")

        db.commit()
        return patrons_models.Patron(
            id=patron_updated[0],
            first_name=patron_updated[1],
            last_name=patron_updated[2],
            email=patron_updated[3],
            registration_date=patron_updated[4]
        )

    except psycopg2.errors.UniqueViolation as e:
        db.rollback()
        raise custom_exceptions.DuplicateEntryException(
            "A patron with the given email already exists."
        )
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to update the patron."
        )
