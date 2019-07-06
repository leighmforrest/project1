# Project 1

Web Programming with Python and JavaScript

## Classic Book Report

## Files

### /app

    ####auth
        * **__init__.py**: file containing code to make **auth** a blueprint package
        * **templates**
        * **forms.py**: file containing WTForms for registration, login and logout
        * **routes.py**: file containing the views for user information
    * **books**
        * **__init__.py**: file containing code to make **books** a blueprint package
        * **templates**
        * **forms.py**: file containing WTForms for ratings
        * **routes.py**: file containing the views for books
    * **books**
        * **__init__.py**: file containing code to make **home** a blueprint package
        * **templates**
        * **routes.py**: file containing the views for the homepage and the book data api
    * **static/css/styles.css**: The compiled css file
    * **templates**: folder containing templates used throughout the app
        * **macros**
            * **_flashmessages.html**: macro to enable flash messages
            * **_formhelpers.html**: macro to allow Bootstrap styles
                to be more consistently displayed in a WTForm
        * **partials**
            **_footer.html**: markup for the footer
            **_link_list.html**: markup for a list of books that link to the books detail page
            **_login_modal.html**: markup for a modal login form
            **_nav.html**

