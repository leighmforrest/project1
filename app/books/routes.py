from flask import redirect, session, request, url_for, flash, render_template, abort


from . import books_blueprint
from app.models import Book
from app.utils.decorators import login_required


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
  book = Book.get_detail_by_isbn(isbn)
  if book:
    return render_template('books/detail.html', book=book)
  else:
    abort(404)


@books_blueprint.route("<string:isbn>/comment", methods=["POST"])
@login_required
def create_comment(isbn):
  return f"CREATE COMMENT FOR {isbn}"


@books_blueprint.route("<string:isbn>/comment/update")
def update_comment(isbn):
  return f"TODO: UPDATE"


@books_blueprint.route("<string:isbn>/comment/delete")
def delete_comment(isbn):
  return f"DELETE COMMENT FOR {isbn}"
