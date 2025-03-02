-- seed_data.sql

-- Insert Authors
INSERT INTO authors (first_name, last_name, date_of_birth) VALUES
('Douglas', 'Adams', '1952-03-11'),
('J.R.R.', 'Tolkien', '1892-01-03'),
('Frank', 'Herbert', '1920-10-08'),
('Isaac', 'Asimov', '1920-01-02'),
('George', 'Orwell', '1903-06-25');

-- Insert Books
-- IMPORTANT :: These isbn numbers are incorrect here
INSERT INTO books (title, isbn, genre, publication_date, available_copies) VALUES
('The Hitchhiker''s Guide to the Galaxy', '9780345391803', 'Science Fiction', '1979-10-12', 5),
('The Lord of the Rings', '9780618260264', 'Fantasy', '1954-07-29', 3),
('Dune', '9780441172719', 'Science Fiction', '1965-08-01', 2),
('Foundation', '9780553293357', 'Science Fiction', '1951-06-01', 4),
('1984', '9780451524935', 'Dystopian', '1949-06-08', 1);

-- Insert Book_Authors (Associate Authors with Books)
INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1),  -- Douglas Adams wrote "The Hitchhiker's Guide..."
(2, 2),  -- J.R.R. Tolkien wrote "The Lord of the Rings"
(3, 3),  -- Frank Herbert wrote "Dune"
(4, 4),  -- Isaac Asimov wrote "Foundation"
(5, 5);  -- George Orwell wrote "1984"

-- Insert Patrons
INSERT INTO patrons (first_name, last_name, email, registration_date) VALUES
('Alice', 'Smith', 'alice.smith@example.com', '2024-01-15'),
('Bob', 'Johnson', 'bob.johnson@example.com', '2024-02-20'),
('Charlie', 'Brown', 'charlie.brown@example.com', '2024-03-01');

-- Insert Loans
INSERT INTO loans (book_id, patron_id, loan_date, due_date) VALUES
(1, 1, '2024-04-01', '2024-04-15'),  -- Alice borrowed "The Hitchhiker's Guide..."
(2, 2, '2024-04-05', '2024-04-19'),  -- Bob borrowed "The Lord of the Rings"
(3, 3, '2024-04-10', '2024-04-24');  -- Charlie borrowed "Dune"

-- Adjust available copies (after loans)
UPDATE books SET available_copies = available_copies - 1 WHERE id IN (1, 2, 3);
