from flask import render_template


from . import home_blueprint
from app.auth.forms import LoginForm
from app.models import Book


@home_blueprint.route('/')
def home():
    login_form = LoginForm()
    books = Book.get_random_books()
    return render_template("home/index.html", login_form=login_form, books=books)
