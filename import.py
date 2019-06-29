import csv

from app.utils.dao import DataAccessObject


BOOK_FIELDS = ['isbn', 'author', 'title', 'year']


def get_data_from_csv(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]
        return data


def add_book(book):
    # Make sure there are no bad fields
    for field in BOOK_FIELDS:
        assert field in book

    # create or add author and get id
    author_query = DataAccessObject.execute("SELECT id FROM authors WHERE name = :name",
                                            {'name': book['author']})

    if author_query.rowcount > 0:
        author_id = author_query.fetchone()[0]
    else:
        DataAccessObject.alter("INSERT INTO authors (name) VALUES (:name)", {'name': book['author']})
        author_id = DataAccessObject.fetchone("SELECT id FROM authors WHERE name = :name",
                                              {'name': book['author']})[0]
        # add book to database
    DataAccessObject.alter("INSERT INTO BOOKS (author_id, title, isbn, year) VALUES (:author_id, :title, :isbn, :year)",
                           {'author_id': author_id, 'title': book['title'], 'isbn': book['isbn'], 'year': book['year']})

    # when data is imported, update for tsvector
    DataAccessObject.alter("""
        UPDATE books SET                                                                                                         tsv = document.tsv FROM (
                SELECT books.id as book_id,
                setweight(to_tsvector(books.title), 'A') || setweight(to_tsvector(authors.name), 'B')|| to_tsvector(books.isbn) || to_tsvector(books.year) AS tsv
                FROM books
                JOIN authors ON authors.id = books.author_id) as document
                WHERE document.book_id = books.id;
    """)


if __name__ == '__main__':
    books = get_data_from_csv('books.csv')
    for book in books:
        print(f"ADDING '{book['title']}'")
        add_book(book)
