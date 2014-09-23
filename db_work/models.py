__author__ = 'cltanuki'
from peewee import *

soc_db = PostgresqlDatabase('soc', user='soc', password='default', host='37.143.13.95')

# soc_db = SqliteDatabase('soc.sqlite')


class Proxy(Model):
    body = CharField(unique=True, index=True)
    level = IntegerField(null=True, default=True)

    class Meta:
        database = soc_db


class TwitterUser(Model):
    url = CharField(unique=True, index=True)
    is_ru = BooleanField(null=True)

    class Meta:
        database = soc_db


class VkUser(Model):
    url = CharField(unique=True, index=True)
    is_ru = BooleanField(null=True)

    class Meta:
        database = soc_db