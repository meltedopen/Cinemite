import datetime
from peewee import *
from flask import jsonify

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
        
    @classmethod
    def create_user(cls, username, email, password, avatar="./static/images/default_avatar.png", admin=False):
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
    user_id = ForeignKeyField(User, backref="list"),
    movie_id = IntegerField(),
    watched = BooleanField(default=False),
    comment = CharField(max_length=600),
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def create_list_item(cls, user_id, movie_id, watched, comment, timestamp):
        new_list_item = List(user_id, movie_id, watched, comment, timestamp)
        try:
            db.session.add(new_list_item)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception('Session rollback')
        return list_schema.jsonify(new_list_item)
            
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()