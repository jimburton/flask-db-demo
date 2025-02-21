from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    username = StringField('name')
    password = PasswordField('password')
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    _id    = IntegerField()
    title  = StringField('title', validators=[DataRequired()])
    body   = TextAreaField('body')
    submit = SubmitField("Save")

