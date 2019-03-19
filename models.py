import datetime
from peewee import *
DATABASE = SqliteDatabase('cinemite.db')


class User(Model):

    username = CharField()
    email = CharField()
    password = CharField()
    avatar = CharField()

    class Meta:
        database = DATABASE


class List(Model):
    user = ForeignKeyField(User, backref='mylist')
    movie = IntegerField()
    watched = BooleanField(default=False)
    comment = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-timestamp', )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, List], safe=True)
    DATABASE.close()
