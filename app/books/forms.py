from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import ValidationError, Length, DataRequired
from app.models import Ratings

CHOICES = ((i, i) for i in range(1, 5))


class RatingForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired(), Length(
        min=1, max=500, message="Username must be between 1 and 500 characters")])
    rating = RadioField('Rating', choices=CHOICES)
