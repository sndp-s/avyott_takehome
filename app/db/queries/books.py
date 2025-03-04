"""
Query wrappers for Books entity.
"""

import psycopg2
from psycopg2.extras import execute_values
from app.db.helpers import \
    execute_sql_fetch_all, execute_sql_fetch_one
from app.models import books as books_models
from app.core import exceptions as custom_exceptions


def get_all_books_query(db, filters, offset, limit):
    """
    Obtain all books with optional filtering.
    """
    try:
        # Prepare the WHERE clause for filtering.
        where_clauses = []
        filter_params = {}
        if filters.title:
            where_clauses.append("b.title ILIKE %(title)s")
            filter_params["title"] = f"%{filters.title}%"
        if filters.genre:
            where_clauses.append("b.genre ILIKE %(genre)s")
            filter_params["genre"] = f"%{filters.genre}%"
        if filters.isbn:
            where_clauses.append("b.isbn ILIKE %(isbn)s")
            filter_params["isbn"] = f"%{filters.isbn}%"
        if filters.author:
            where_clauses.append("""
                EXISTS (
                    SELECT 1 FROM authors a2 
                    JOIN book_authors ba2 ON b.id = ba2.book_id 
                    WHERE a2.id = ba2.author_id 
                    AND (a2.first_name ILIKE %(author)s OR a2.last_name ILIKE %(author)s)
                )
            """)
            filter_params["author"] = f"%{filters.author}%"

        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

        params = {"limit": limit, "offset": offset}
        params.update(filter_params)

        # Prepare the main query.
        sql = f"""
            SELECT * FROM (
                SELECT 
                    b.id, 
                    b.title, 
                    b.isbn, 
                    b.genre, 
                    b.publication_date, 
                    COALESCE(
                        json_agg(
                            DISTINCT jsonb_build_object(
                                'id', a.id, 
                                'first_name', a.first_name, 
                                'last_name', a.last_name
                            )
                        ) FILTER (WHERE a.id IS NOT NULL), 
                        '[]'::json
                    ) AS authors
                FROM books b
                LEFT JOIN book_authors ba ON b.id = ba.book_id
                LEFT JOIN authors a ON ba.author_id = a.id
                {where_clause}
                GROUP BY b.id
                ORDER BY b.title
            ) AS sub
            LIMIT %(limit)s OFFSET %(offset)s;
        """
        all_books = execute_sql_fetch_all(db, sql, params)
        return all_books
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to fetch books."
        )


def get_book(db, book_id):
    """
    Fetch the book matching the given id
    """
    try:
        sql = \
        """
        SELECT 
            b.id, 
            b.title, 
            b.isbn, 
            b.genre, 
            b.publication_date,
            b.available_copies,
            COALESCE(
                json_agg(
                    DISTINCT jsonb_build_object(
                        'id', a.id, 
                        'first_name', a.first_name, 
                        'last_name', a.last_name
                    )
                ) FILTER (WHERE a.id IS NOT NULL), 
                '[]'::json
            ) AS authors
        FROM books b
        LEFT JOIN book_authors ba ON b.id = ba.book_id
        LEFT JOIN authors a ON ba.author_id = a.id
        WHERE b.id = %(book_id)s
        GROUP BY b.id;
        """
        params = {'book_id': book_id}
        book = execute_sql_fetch_one(db, sql, params)
        if not book:
            raise custom_exceptions.RecordNotFoundException("Books not found")
        return book
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to fetch the book."
        )


def add_new_book(db, book: books_models.BookCreate) -> int:
    """
    Add a new book record to the database and link it to the provided authors.
    Returns the newly created book's ID.
    """
    try:
        with db.cursor() as cursor:
            # Insert the book into the books table
            book_sql = """
            INSERT INTO books (title, isbn, genre, publication_date, available_copies)
            VALUES (%(title)s, %(isbn)s, %(genre)s, %(publication_date)s, %(available_copies)s)
            RETURNING id;
            """
            params = {
                'title': book.title,
                'isbn': book.isbn,
                'genre': book.genre,
                'publication_date': book.publication_date,
                'available_copies': book.available_copies,
            }
            cursor.execute(book_sql, params)
            new_book_id_row = cursor.fetchone()
            new_book_id = new_book_id_row[0]

            # Link the new book with each provided author via book_authors table
            link_sql = """
            INSERT INTO book_authors (book_id, author_id)
            VALUES (%(book_id)s, %(author_id)s);
            """
            for author_id in book.author_ids:
                link_params = {
                    'book_id': new_book_id,
                    'author_id': author_id,
                }
                cursor.execute(link_sql, link_params)

        # Commit the transaction only if all the previous operations succeed
        db.commit()
        return new_book_id

    except psycopg2.errors.UniqueViolation as e:
        db.rollback()
        raise custom_exceptions.DuplicateEntryException(
            "A book with the given ISBN already exists."
        )
    except psycopg2.errors.ForeignKeyViolation as e:
        db.rollback()
        raise custom_exceptions.ForeignKeyNotFoundException(
            "The specified author was not found. Please check the author ID and try again."
        )
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to add the book to the library."
        )


def update_book(db, book_id, update_data):
    """
    Update a book record and its associated authors.
    """
    try:
        with db.cursor() as cursor:
            # Prepare the UPDATE statement for book fields (excluding 'author_ids')
            set_clauses = []
            params = {}
            for key, value in update_data.items():
                if key != "author_ids":
                    set_clauses.append(f"{key} = %({key})s")
                    params[key] = value
            params["book_id"] = book_id

            book_updated = False
            if set_clauses:
                sql_update = f"""
                UPDATE books
                SET {', '.join(set_clauses)}
                WHERE id = %(book_id)s
                RETURNING id;
                """
                cursor.execute(sql_update, params)
                book_updated = cursor.fetchone()

            if not book_updated:
                raise custom_exceptions.RecordNotFoundException("The book with the given ID does not exist.")

            # If author_ids is provided, update the book_authors associations
            if "author_ids" in update_data:
                new_author_ids = update_data["author_ids"]
                # Delete existing associations
                cursor.execute("DELETE FROM book_authors WHERE book_id = %(book_id)s;",
                               {"book_id": book_id})
                # Bulk insert new associations
                bulk_sql = "INSERT INTO book_authors (book_id, author_id) VALUES %s;"
                values = [(book_id, author_id) for author_id in new_author_ids]
                execute_values(cursor, bulk_sql, values)
        
        # Commit transaction if all operations succeed
        db.commit()
        return book_id
    except psycopg2.errors.UniqueViolation as e:
        db.rollback()
        raise custom_exceptions.DuplicateEntryException(
            "A book with the given ISBN already exists."
        )
    except psycopg2.errors.ForeignKeyViolation as e:
        db.rollback()
        raise custom_exceptions.ForeignKeyNotFoundException(
            "The specified author was not found. Please check the author ID and try again."
        )
    except psycopg2.Error as e:
        db.rollback()
        raise custom_exceptions.DatabaseOperationException(
            "Failed to update the book."
        )


# NOTE :: Fix the deletion logic
def delete_book(db, book_id: int) -> int:
    """
    Delete a book and its associations from the database.
    """
    try:
        with db.cursor() as cursor:
            # Delete associations in book_authors table
            cursor.execute("DELETE FROM book_authors WHERE book_id = %(book_id)s", {"book_id": book_id})

            # Delete the book from the books table
            cursor.execute("DELETE FROM books WHERE id = %(book_id)s", {"book_id": book_id})

        db.commit()
        return True
    except psycopg2.errors.ForeignKeyViolation as e:
        db.rollback()
        raise custom_exceptions.LoanPendingException("Cannot delete book as it is currently loaned.")
    except psycopg2.Error as e:
        db.rollback()
        raise
