from functools import wraps
from flask import session, request, redirect, url_for, abort, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            flash('Please login to continue', 'warning')
            return redirect(url_for('home.home'))
        return f(*args, **kwargs)
    return decorated_function
