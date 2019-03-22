import datetime
from peewee import *

from flask import Flask, g
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('cinemite.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    avatar = CharField()
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    def get_list(self):
        return List.select().where(List.user_id == self)

    @classmethod
    def create_user(cls, username, email, password, avatar="../static/images/default_avatar.png", admin=False):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                is_admin=admin,
                avatar=avatar)
        except IntegrityError:
            raise ValueError("User already exists")


class List(Model):
    user = ForeignKeyField(
        model=User,
        backref="lists")
    movie_id = IntegerField()
    watched = BooleanField(default=False)
    comment = CharField(max_length=600, default='')
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        indexes = ((("user_id", "movie_id"), True),)

    @classmethod
    def create_list_item(cls, user_id, movie_id):
        try:
            cls.create(
                user=user_id,
                movie_id=movie_id
            )
        except IntegrityError:
            raise

    # @classmethod
    # def delete_list_item(cls, user_id, movie_id):
    #     cls.delete_instance().where(cls.user == user_id and cls.movie_id == movie_id).execute()


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, List], safe=True)
    DATABASE.close()
