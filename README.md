# Project 1

Web Programming with Python and JavaScript

## Classic Book Report

This website allows users to search and rate curated books, and see how they are rated on the Goodreads platform.

## Files

### /app

#### auth

* **__init__.py**: file containing code to make **auth** a blueprint package
* **templates**
* **forms.py**: file containing WTForms for registration, login and logout
* **routes.py**: file containing the views for user information

#### books
* **__init__.py**: file containing code to make **books** a blueprint package
* **templates**
* **forms.py**: file containing WTForms for ratings
* **routes.py**: file containing the views for books

#### home
* **__init__.py**: file containing code to make **home** a blueprint package
* **templates**
* **routes.py**: file containing the views for the homepage and the book data api

#### static/css/styles.css: The compiled css file

* **templates**: folder containing templates used throughout the app
* **macros**
    * **_flashmessages.html**: macro to enable flash messages
    * **_formhelpers.html**: macro to allow Bootstrap styles
        to be more consistently displayed in a WTForm
* **partials**
    * **_footer.html**: markup for the footer
    * **_link_list.html**: markup for a list of books that link to the books detail page
    * **_login_modal.html**: markup for a modal login form
    * **_nav.html**: markup for the navbar
    * **_rating_modal.html**: markup for the rating form
* **base.html**: The base template

#### /utils
* **__init__.py**: file to make utils a package
* **dao.py**: script for basic database actions
* **decorators.py**: script for application decorators. Used mainly for authenticating routes
* **__init__.py**: makes the app folder a package. Contains the [application factory function](http://flask.pocoo.org/docs/1.0/patterns/appfactories/)

### /scss
**styles.scss**: the SASS file for the web application

### /

**app.sql**: SQL file for the the application

**application.py**: The script that runs the application

**books.csv**: The data for the curated list

**config.py**: Configuration for the application

**import.py**: File for importing the csv data into the datbase

**Procfile**: File used to run the app on Heroku

**reuqirements.txt**: List of Python modules required for the appliction 

## Environment Variables

**DATABASE_URL**: The url where the database is accessed

**FLASK_APP**: The file where the application is run. In this case, it's application.py

**FLASK_CONFIG**: The name of the configuration. They are in the dictionary in config.py

**GOODREADS_KEY**: The goodreads API key

**SECRET_KEY**: String of characters needed for having sessions enabled

## Works Cited

Escobar, Jorge. (https://github.com/esfoobar/flogger)[Flogger]. Accessed July 4, 2019.

Nzomo, Mbithe. (https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one) [Build a CRUD Web App With Python and Flask - Part One]. December 20, 2016. Accesed July 4, 2019.