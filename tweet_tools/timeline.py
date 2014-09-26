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

    class Meta:
        database = db


def main():
    db.connect()
    db.create_table(Rows, safe=True)
    api = TwitterAPI('65dxiPhn10SE3zJT6fVEPWsVx', 'VmK0rQFapjymwtSNpidi0Yfe16mjMdHXBhZTmYVc8dwb1joAxX',
                     '109566527-ZufkixJ3XInW91ZE34hGFtxQcrXGOzBS7vBdApUP', '0N5poNnJoDsWO8Yvf1FfNECfOJKJm7nKthPVzow7apyPu')
    user_ids = [x.twi_id for x in Tweeple.select().where(Tweeple.filled_tweets == 0)]
    counter = 0
    bad_conter = 0
    iter = len(user_ids)
    print(iter)
    sleep(15*60)
    for twi_id in user_ids:
        r = api.request('statuses/user_timeline', {'user_id': twi_id, 'count': '100'})
        with db.transaction():
            user = Tweeple.get(twi_id=twi_id)
            for tweet in r:
                tweet['user'] = user
                if 'id' not in tweet.keys():
                    iter -= 1
                    counter += 1
                    bad_conter += 1
                    print(iter, 'Bad')
                    continue
                del tweet['id']
                Rows.create(**tweet)
            user.filled_tweets = 1
            user.save()
        counter += 1
        if counter > 290:
            sleep(15*60)
            counter = 0
        iter -= 1
        print(iter)
    print(bad_conter)


if __name__ == '__main__':
    main()