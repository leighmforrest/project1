from flask import redirect, session, request, url_for, flash, render_template, abort


from . import books_blueprint
from app.models import Book, Rating, User
from app.utils.decorators import login_required
from .forms import RatingForm


@books_blueprint.route("/", methods=["GET"])
@login_required
def search():
  query_string = request.args.get('q')
  page = int(request.args.get('page') or 1)
  queryset = Book.search_for_books(query_string, page)
  max_pages = int(queryset['max_pages'])
  is_next = page < max_pages
  return render_template('books/search.html',
                         books=queryset['results'],
                         page=page,
                         query_string=query_string,
                         max_pages=max_pages,
                         is_next=is_next)


@books_blueprint.route("/<string:isbn>", methods=["GET"])
@login_required
def detail(isbn):
  # get data
  user_id = User.get_user_id(session['username'])
  book = Book.get_detail_by_isbn(isbn)
  book_id = Book.get_id_by_isbn(isbn)
  ratings = Rating.get_ratings_by_isbn(isbn)
  has_rating = Rating.check_rating(user_id, book_id)

  # initialize form
  if has_rating:
    form = RatingForm()
  else:
    rating = Rating.get_rating_by_user_id(user_id, book_id)
    form = RatingForm()
    form.rating.data = str(rating[0])
    form.comment.data = rating[1]

  if book:
    return render_template('books/detail.html', book=book, isbn=isbn, form=form, ratings=ratings, has_rating=has_rating)
  else:
    abort(404)


@books_blueprint.route("<string:isbn>/comment", methods=["POST"])
@login_required
def create_comment(isbn):
  form = RatingForm(request.form)
  username = session['username']
  if form.validate_on_submit():
    Rating.add_rating(username, isbn, form.rating.data, form.comment.data)
    flash("Comment added.", "success")
  else:
    flash("Rating could not be added", "warning")
  return redirect(url_for('books.detail', isbn=isbn))


@books_blueprint.route("<string:isbn>/comment/update", methods=["POST"])
@login_required
def update_comment(isbn):
  form = RatingForm(request.form)
  username = session['username']
  if form.validate_on_submit():
    Rating.update_rating(username, isbn, form.rating.data, form.comment.data)
    # print(updated)
    flash("Comment added.", "success")
  else:
    print(form.errors)
    flash("Rating could not be added", "warning")
  return redirect(url_for('books.detail', isbn=isbn))


@books_blueprint.route("<string:isbn>/comment/delete", methods=["POST"])
@login_required
def delete_comment(isbn):
  username = session['username']
  Rating.delete_rating(username, isbn)
  flash("Rating deleted", "danger")
  return redirect(url_for('books.detail', isbn=isbn))
