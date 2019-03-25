from flask_wtf import FlaskForm as Form

from models import User
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                                Length, EqualTo)


def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class CommentForm(Form):
    comment = CKEditorField(
        'Write a review',
        validators=[
            DataRequired()
        ])


class UserForm(Form):
    username = StringField(
        'Edit your username',
        validators=[
            DataRequired()
        ])
    email = StringField(
        'Edit your email',
        validators=[
            DataRequired()
        ])
    password = StringField(
        'Edit your password',
        validators=[
            DataRequired()
        ])


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Username should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
