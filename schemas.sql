-- Drop tables if they already exist
DROP TABLE IF EXISTS loans CASCADE;

DROP TABLE IF EXISTS book_authors CASCADE;

DROP TABLE IF EXISTS books CASCADE;

DROP TABLE IF EXISTS authors CASCADE;

DROP TABLE IF EXISTS patrons CASCADE;

-- Create new tables
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    date_of_birth DATE
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    genre VARCHAR(255),
    publication_date DATE,
    available_copies INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE book_authors (
    book_id INTEGER REFERENCES books (id) ON DELETE CASCADE,
    author_id INTEGER REFERENCES authors (id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE patrons (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books (id) ON DELETE RESTRICT,
    patron_id INTEGER REFERENCES patrons (id) ON DELETE RESTRICT,
    loan_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE
);
