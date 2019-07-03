from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, max=25,
               message="Username must be between 5 and 25 characters")])
    handle = StringField('Handle', validators=[
        Length(max=25, message="Handle cannot exceed 25 characters")])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=25,
               message="Password must be between 8 and 25 characters")])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password')])

    def validate_username(self, username):
        if User.user_exists(self.username.data):
            raise ValidationError('Please use a different username')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        if User.login(self.username.data, self.password.data):
            return True
        else:
            self.password.errors.append('Incorrect email or password')


class EditUserForm(FlaskForm):
    handle = StringField('Handle', validators=[
        Length(max=25, message="Handle cannot exceed 25 characters")])
