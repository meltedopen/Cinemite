from flask_wtf import FlaskForm as Form
from wtforms import TextField, TextAreaField, SubmitField

from models import User, List


class CommentForm(Form):
    text = TextField('What did you think of the movie?')
    submit = SubmitField('Submit')


class UserForm(Form):
    username = CharField('Username')
    email = CharField('Email')
    password = CharField('Password')
    avatar = CharField('Profile Image')
