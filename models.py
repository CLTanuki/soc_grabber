__author__ = 'cltanuki'
from peewee import *

db = SqliteDatabase('people.db')


class TwitterUser(Model):
    screenname = CharField()
    url = CharField()
    is_ru = BooleanField(null=True)

    class Meta:
        database = db  # модель будет использовать базу данных 'people.db'