from flask import render_template, jsonify, abort


from . import home_blueprint
from app.auth.forms import LoginForm
from app.models import Book, goodreads


@home_blueprint.route('/')
def home():
    login_form = LoginForm()
    books = Book.get_random_books()
    return render_template("home/index.html",
                           login_form=login_form,
                           books=books)


@home_blueprint.route("/api/<string:isbn>", methods=["GET"])
def get_book_data(isbn):
    # get book data
    book = Book.get_detail_by_isbn(isbn)

    if book is None:
        abort(404)
    else:
        data = {}
        # get goodreads data
        goodreads_data = goodreads(isbn)

        # fill dict
        data['name'] = book.name
        data['title'] = book.title
        data['year'] = book.year
        data['isbn'] = book.isbn
        data['average_score'] = float(goodreads_data['average_rating'])
        data['review_count'] = int(goodreads_data['work_ratings_count'])
        return jsonify(data)
