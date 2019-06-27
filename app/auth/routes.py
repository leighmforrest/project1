from flask import redirect, session, request, url_for, flash, render_template

from . import auth_blueprint


@auth_blueprint.route("/dashboard")
def dashboard():
    return "DASHBOARD"


@auth_blueprint.route("/login")
def login():
    return "LOGIN"


@auth_blueprint.route("/logout")
def logout():
    return "LOGOUT"
