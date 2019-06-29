import sys
from flask import redirect, session, request, url_for, flash, render_template

from . import auth_blueprint
from .forms import RegistrationForm, LoginForm
from app.utils.decorators import login_required
from app.models import User


@auth_blueprint.route("/dashboard")
@login_required
def dashboard():
    return "DASHBOARD"


@auth_blueprint.route('/login', methods=["POST"])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('home.home'))
    else:
        flash('Username or password incorrect', 'warning')
        return redirect(url_for('home.home'))


@auth_blueprint.route("/logout")
@login_required
def logout():
    session.pop('username')
    flash("You have been logged out.", 'success')
    return redirect(url_for('home.home'))


@auth_blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        if User.register(form.username.data, form.password.data, form.handle.data):
            flash("User successfully registered", "success")
        else:
            flash("Could not register user", "warning")
        return redirect(url_for('home.home'))
    else:
        return render_template("auth/register.html", form=form)
