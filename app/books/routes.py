from flask import redirect, session, request, url_for, flash, render_template


from . import books_blueprint


@books_blueprint.route("/")
def search():
    return "SEARCH TODO:QUERYSTRING"


@books_blueprint.route("/<string:isbn>")
def detail(isbn):
    return f"ISBN:{isbn}"


@books_blueprint.route("<string:isbn>/comment")
def create_comment(isbn):
    return f"CREATE COMMENT FOR {isbn}"


@books_blueprint.route("<string:isbn>/comment/update")
def update_comment(isbn):
    return f"TODO: UPDATE"


@books_blueprint.route("<string:isbn>/comment/delete")
def delete_comment(isbn):
    return f"DELETE COMMENT FOR {isbn}"
