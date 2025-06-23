"""
The forms used by the app.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    """ The class for the login and registration forms."""
    username = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    """ The class for the forms relating to blog posts."""
    _id    = IntegerField()
    title  = StringField('title', validators=[DataRequired()])
    body   = TextAreaField('body', validators=[DataRequired()])
    submit = SubmitField("Save")
