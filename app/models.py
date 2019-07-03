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
            DataAccessObject.alter(
                "INSERT INTO users(username, password, handle) VALUES (:username, :password, :handle)", {'username': username, 'password': password, 'handle': handle})
            return True
        else:
            return False

    @classmethod
    def user_exists(cls, username):
        return DataAccessObject.rowcount("SELECT username from users WHERE username = :username",
                                         {'username': username}) == 1

    @classmethod
    def get_user_id(cls, username):
        user = DataAccessObject.fetchone("SELECT id from users WHERE username = :username",
                                         {'username': username})
        return user[0]

    @classmethod
    def get_user_data(cls, username):
        user = DataAccessObject.fetchone("SELECT username, handle from users WHERE username = :username", {
            'username': username})
        return user

    @classmethod
    def login(cls, username, password):
        user = DataAccessObject.fetchone("SELECT username, password FROM users WHERE username=:username",
                                         {'username': username})
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
    def change_handle(cls, username, handle):
        if DataAccessObject.rowcount('SELECT username FROM users WHERE username = :username',
                                     {'username': username}) > 0:
            DataAccessObject.alter("UPDATE users SET handle = :handle WHERE username = :username",
                                   {'username': username, 'handle': handle})
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
        book = DataAccessObject.fetchone("""
        SELECT books.id
        FROM books
        WHERE books.isbn= :isbn
        """, {'isbn': isbn})
        if book:
            return int(book[0])
        else:
            return None


class Rating:
    @classmethod
    def add_rating(cls, username, isbn, rating, comment):
        user_id = User.get_user_id(username)
        book_id = Book.get_id_by_isbn(isbn)
        rating = int(rating)
        if user_id and book_id and Rating.check_rating(user_id, book_id):
            DataAccessObject.alter("INSERT INTO ratings(user_id, book_id, rating, comment) VALUES (:user_id, :book_id, :rating, :comment)", {'user_id': user_id, 'book_id': book_id, 'rating': rating, 'comment': comment})
            return True
        else:
            return False

    @classmethod
    def check_rating(cls, user_id, book_id):
        """Check if user has left a rating. Return false if review was left."""
        return DataAccessObject.rowcount("SELECT * from ratings WHERE (user_id=:user_id AND book_id=:book_id)", {'user_id': user_id, 'book_id': book_id}) == 0

    @classmethod
    def update_rating(cls, username, isbn, rating, comment):
        user_id = User.get_user_id(username)
        book_id = Book.get_id_by_isbn(isbn)
        rating = int(rating)
        if user_id and book_id and not Rating.check_rating(user_id, book_id):
            DataAccessObject.alter("""
                UPDATE ratings SET comment=:comment, rating=:rating
                WHERE (user_id=:user_id AND book_id=:book_id)""",
                                   {'user_id': user_id,
                                    'book_id': book_id,
                                    'comment': comment,
                                    'rating': rating})
            return True
        else:
            return False

    @classmethod
    def get_ratings_by_isbn(cls, isbn):
        book_id = Book.get_id_by_isbn(isbn)
        if book_id is not None:
            return DataAccessObject.fetchall("""
                SELECT users.handle, ratings.rating, ratings.comment
                FROM ratings
                JOIN users ON users.id=ratings.user_id
                WHERE ratings.book_id=:book_id
            """, {'book_id': book_id})
        else:
            return None

    @classmethod
    def get_rating_by_user_id(cls, user_id, book_id):
        return DataAccessObject.fetchall("""
                SELECT ratings.rating, ratings.comment
                FROM ratings
                WHERE user_id=:user_id AND book_id=:book_id
            """, {'user_id': user_id, 'book_id': book_id})[0]

    @classmethod
    def delete_rating(cls, username, isbn):
        user_id = User.get_user_id(username)
        book_id = Book.get_id_by_isbn(isbn)
        if user_id and book_id and not Rating.check_rating(user_id, book_id):
            DataAccessObject.alter("""
                DELETE FROM ratings
                WHERE (user_id=:user_id AND book_id=:book_id)""",
                                   {'user_id': user_id, 'book_id': book_id})
            return True
        else:
            return False
