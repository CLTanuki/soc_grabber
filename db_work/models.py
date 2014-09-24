__author__ = 'cltanuki'
from peewee import *

soc_db = PostgresqlDatabase(database='soc', user='soc', password='default', host='37.143.13.95')


class Proxy(Model):
    body = CharField(max_length=15, unique=True, index=True)
    level = IntegerField(null=True, default=True)

    class Meta:
        database = soc_db


class TwitterUser(Model):
    id_str = CharField(unique=True, index=True)
    is_ru = BooleanField(null=True)

    class Meta:
        database = soc_db


class VkUser(Model):
    id_str = BigIntegerField(unique=True, index=True)
    is_ru = BooleanField(null=True)
    deactivated = BooleanField(null=True)

    class Meta:
        database = soc_db


class VkUserInfo(Model):
    user = ForeignKeyField(rel_model=VkUser)
    screen_name = CharField(null=True)
    photo_50 = CharField(null=True)
    profile_fill_count = IntegerField(null=True)
    country = IntegerField(null=True)
    bdate = CharField(max_length=10, null=True)
    last_seen = CharField()
    added_media_count = IntegerField()
    followers_count = IntegerField()
    has_mobile = BooleanField()
    post_count = IntegerField(null=True)
    friends_count = IntegerField(null=True)

    class Meta:
        database = soc_db


class VkPosts:

    class Meta:
        database = soc_db