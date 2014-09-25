__author__ = 'cltanuki'
from TwitterAPI import TwitterAPI
from peewee import *
from os import _exit
from time import sleep


db = SqliteDatabase('slon.sqlite')


class Tweeple(Model):
    twi_id = IntegerField()

    class Meta:
        database = db


class Rows(Model):
    user = ForeignKeyField(Tweeple)
    id_str = CharField(null=True)
    geo = CharField(null=True)
    created_at = CharField(null=True)
    entities = CharField(null=True)
    source = CharField(null=True)
    contributors = CharField(null=True)
    favorited = CharField(null=True)
    truncated = CharField(null=True)
    lang = CharField(null=True)
    in_reply_to_user_id = CharField(null=True)
    coordinates = CharField(null=True)
    place = CharField(null=True)
    in_reply_to_status_id = CharField(null=True)
    retweeted = CharField(null=True)
    retweet_count = CharField(null=True)
    text = CharField(null=True)
    favorite_count = CharField(null=True)


db.connect()
db.create_table(Rows, safe=True)
api = TwitterAPI('65dxiPhn10SE3zJT6fVEPWsVx', 'VmK0rQFapjymwtSNpidi0Yfe16mjMdHXBhZTmYVc8dwb1joAxX',
                 '109566527-ZufkixJ3XInW91ZE34hGFtxQcrXGOzBS7vBdApUP', '0N5poNnJoDsWO8Yvf1FfNECfOJKJm7nKthPVzow7apyPu')

user_ids = [x.twi_id for x in Tweeple.select()]
counter = 0

for twi_id in user_ids:
    r = api.request('statuses/user_timeline', {'user_id': twi_id, 'count': '100'})
    with db.transaction():
        for tweet in r:
            user = Tweeple.get(twi_id=twi_id)
            del tweet['id']
            del tweet['user']
            print(tweet)
            Rows.create(**tweet)
    counter += 1
    if counter > 300:
        sleep(15*60)
        counter = 0
    print('+1')