__author__ = 'cltanuki'
from peewee import *

meta_db = SqliteDatabase('meta.db')
tweet_db = SqliteDatabase('twitter.db')
vk_db = SqliteDatabase('vk.db')


class Proxy(Model):
    type = CharField(max_length=5)
    body = CharField(max_length=25, unique=True)

    class Meta:
        database = meta_db


class TwitterUser(Model):
    screenname = CharField()
    url = CharField(unique=True)
    is_ru = BooleanField(null=True)

    class Meta:
        database = tweet_db


class VkUser(Model):
    nickname = CharField()
    url = CharField(unique=True)
    is_ru = BooleanField(null=True)

    class Meta:
        database = vk_db