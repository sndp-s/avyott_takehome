"""
Query wrappers for Books entity.
"""

from app.db.helpers import execute_sql_fetch_all


def get_all_books_query(db, filters, offset, limit):
    """
    Obtain all books
    """
    # TODO :: Add filtering
    sql = \
        """
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
            GROUP BY b.id
            ORDER BY b.title
        ) AS sub
        LIMIT %(limit)s OFFSET %(offset)s;
        """
    params = {'limit': limit, 'offset': offset}
    all_books = execute_sql_fetch_all(db, sql, params)
    return all_books
