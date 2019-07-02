from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField
from wtforms.validators import Length, DataRequired


CHOICES = [(str(i), str(i)) for i in range(1, 6)]


class RatingForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[
        DataRequired(),
        Length(min=1, max=500, message="Username must be between 1 and 500 characters")])
    rating = RadioField('Rating', choices=CHOICES, default='4')


class DeleteRatingForm(FlaskForm):
    pass
