from flask import redirect, session, request, url_for, flash, render_template


from . import home_blueprint
from app.auth.forms import RegistrationForm, LoginForm


@home_blueprint.route('/')
def home():
    login_form = LoginForm()
    return render_template("home/index.html", login_form=login_form)
