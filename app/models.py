from math import ceil

from .utils.dao import DataAccessObject
from . import bcrypt


MAX_BOOKS_PER_PAGE = 5


class User:
    @classmethod
    def register(cls, username, password, handle=''):
        if not User.user_exists(username):
            # encrypt password for save
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            DataAccessObject.alter("INSERT INTO users(username, password, handle) VALUES (:username, :password, :handle)", {'username': username, 'password': password, 'handle': handle})
            return True
        else:
            return False

    @classmethod
    def user_exists(cls, username):
        return DataAccessObject.rowcount("SELECT username from users WHERE username = :username", {
            'username': username}) == 1

    @classmethod
    def get_user_id(cls, username):
        return DataAccessObject.fetchone("SELECT id from users WHERE username = :username", {
            'username': username})[0]

    @classmethod
    def login(cls, username, password):
        user = DataAccessObject.fetchone("SELECT username, password FROM users WHERE username=:username", {'username': username})
        if not user:
            return False
        else:
            return bcrypt.check_password_hash(user['password'], password)

    @classmethod
    def change_password(cls, username, password):
        user = DataAccessObject.fetchone('SELECT username FROM users WHERE username = :username',
                                         {'username': username, 'password': password})
        if user:
            password = bcrypt.generate_password_hash(password).decode("utf-8")
            DataAccessObject.alter("UPDATE users SET password = :password WHERE username = :username",
                                   {'username': username, 'password': password})
            return True
        else:
            return False

    @classmethod
    def change_user_data(cls, username, new_username, handle):
        if User.user_exists(username):
            DataAccessObject.alter("UPDATE users SET username = :new_username, handle = :handle WHERE username = :username",
                                   {'username': username, 'new_username': username, 'handle': handle})
            return True
        else:
            return False


class Book:
    @classmethod
    def get_random_books(cls):
        return DataAccessObject.fetchall("SELECT authors.name, books.title, books.isbn from books JOIN authors ON authors.id=books.author_id  ORDER BY RANDOM() LIMIT :max;",
                                         {'max': MAX_BOOKS_PER_PAGE})

    @classmethod
    def search_for_books(cls, query, page=1):
        limit = MAX_BOOKS_PER_PAGE

        results = DataAccessObject.fetchall("""
        SELECT authors.name, books.title,books.isbn
        FROM books
        JOIN authors
        ON authors.id = books.author_id
        WHERE books.tsv @@ plainto_tsquery(:q)
        """,
                                            {'q': query})
        # make sure page does not exceed page count
        max_pages = ceil(len(results) / MAX_BOOKS_PER_PAGE)
        if page > max_pages:
            page = max_pages

        # return a slice;
        offset = (page - 1) * limit
        return {'max_pages': max_pages, 'results': results[offset:limit + offset]}

    @classmethod
    def get_detail_by_isbn(cls, isbn):

        return DataAccessObject.fetchone("""
        SELECT authors.name, books.title,books.isbn
        FROM books
        JOIN authors
        ON authors.id = books.author_id
        WHERE books.isbn= :isbn
        """,
                                         {'isbn': isbn})

    @classmethod
    def get_id_by_isbn(cls, isbn):
        return DataAccessObject.fetchone("""
        SELECT books.id
        FROM books
        WHERE books.isbn= :isbn
        """, {'isbn': isbn})[0]


class Rating:
    @classmethod
    def add_rating(cls, username, isbn, rating, comment):
        user_id = User.get_user_id(username)
        book_id = Book.get_id_by_isbn(isbn)
        rating = int(rating)
        if user_id and book_id and not Rating.check_rating(user_id, book_id):
            DataAccessObject.alter("INSERT INTO ratings(user_id, book_id, rating, comment) VALUES (:user_id, :book_id, :rating, :comment)", {'user_id': user_id, 'book_id': book_id, 'rating': rating, 'comment': comment})
            return True
        else:
            return False

    @classmethod
    def check_rating(cls, user_id, book_id):
        return DataAccessObject.rowcount("SELECT * from ratings WHERE (user_id=:user_id AND book_id=:book_id)", {'user_id': user_id, 'book_id': book_id})
