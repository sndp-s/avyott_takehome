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


def borrow_book_query(db, patron_id, book_id):
    """
    Lend the book to the patron.
    """
    try:
        with db.cursor() as cursor:
            # Check if the book exists and has available copies
            sql_check_book = """
            SELECT available_copies FROM books WHERE id = %(book_id)s FOR UPDATE;
            """
            cursor.execute(sql_check_book, {"book_id": book_id})
            book = cursor.fetchone()

            if not book:
                raise custom_exceptions.RecordNotFoundException("Book does not exist.")

            available_copies = book[0]
            if available_copies <= 0:
                raise custom_exceptions.UnavailableResourceException("No available copies left for this book.")

            # Check if the patron already has a pending loan for this book
            sql_check_existing_loan = """
            SELECT id FROM loans WHERE patron_id = %(patron_id)s AND book_id = %(book_id)s AND return_date IS NULL;
            """
            cursor.execute(sql_check_existing_loan, {"patron_id": patron_id, "book_id": book_id})
            existing_loan = cursor.fetchone()

            if existing_loan:
                raise custom_exceptions.BusinessValidationException("User already has this book on loan.")

            # Reduce available copies (relying on DB constraints to prevent negative values)
            sql_update_copies = """
            UPDATE books SET available_copies = available_copies - 1 WHERE id = %(book_id)s;
            """
            cursor.execute(sql_update_copies, {"book_id": book_id})

            # Insert new loan record
            sql_create_loan = """
            INSERT INTO loans (patron_id, book_id, loan_date, due_date)
            VALUES (%(patron_id)s, %(book_id)s, CURRENT_DATE, CURRENT_DATE + INTERVAL '14 days')
            RETURNING id;
            """
            cursor.execute(sql_create_loan, {"patron_id": patron_id, "book_id": book_id})
            loan_id = cursor.fetchone()[0]

        # Commit transaction only if all operations succeed
        db.commit()
        return loan_id

    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException("Failed to lend book")


def return_book(db, patron_id, book_id):
    """
    Process the return of a borrowed book.
    """
    try:
        with db.cursor() as cursor:
            # Ensure that the book was actually loaned by the user and is not already returned
            sql_check_loan = """
            SELECT id FROM loans 
            WHERE patron_id = %(patron_id)s 
              AND book_id = %(book_id)s 
              AND return_date IS NULL 
            FOR UPDATE;
            """
            cursor.execute(sql_check_loan, {"patron_id": patron_id, "book_id": book_id})
            loan = cursor.fetchone()

            if not loan:
                raise custom_exceptions.RecordNotFoundException("No active loan found for this book.")

            loan_id = loan[0]

            # Mark the return field in the loan table
            sql_mark_return = """
            UPDATE loans 
            SET return_date = CURRENT_DATE 
            WHERE id = %(loan_id)s;
            """
            cursor.execute(sql_mark_return, {"loan_id": loan_id})

            # Bump up the available copies count for the said book
            sql_update_copies = """
            UPDATE books 
            SET available_copies = available_copies + 1 
            WHERE id = %(book_id)s;
            """
            cursor.execute(sql_update_copies, {"book_id": book_id})

        # Commit transaction only if all operations succeed
        db.commit()

    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException("Failed to return book")
