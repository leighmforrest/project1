import os

from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt

from config import app_config

# extension variables
sess = Session()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    # get private config setting here
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

    # set up extensions and blueprints
    init_extensions(app)
    init_blueprints(app)

    return app


def init_extensions(app):
    sess.init_app(app)
    bcrypt.init_app(app)

    return app


def init_blueprints(app):
    from .home import home_blueprint
    from .auth import auth_blueprint
    from .books import books_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(books_blueprint, url_prefix="/books")
