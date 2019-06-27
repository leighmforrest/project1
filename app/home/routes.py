from flask import redirect, session, request, url_for, flash, render_template


from . import home_blueprint
from app.models import get_data

@home_blueprint.route('/')
def home():
    data = get_data()
    return render_template("home/index.html", data=data)
