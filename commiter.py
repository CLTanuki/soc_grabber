__author__ = 'cltanuki'
from os import path
from time import sleep
from models import tweet_db, TwitterUser


class Commiter():

    def __init__(self, profile_queue):
        self.profile_queue = profile_queue
        self.profile_list = []

    def get_profile_links(self):
        while not self.profile_queue.empty():
            self.profile_list.append(self.profile_queue.get())

    def main(self):
        if not path.isfile('twitter.db'):
            tweet_db.connect()
            tweet_db.create_table(TwitterUser)
        self.get_profile_links()
        if not self.profile_list:
            sleep(30)
            self.main()
        else:
            with tweet_db.transaction():
                TwitterUser.insert_many(self.profile_list).execute()
            print('Commited: ' + str(len(self.profile_list)))
            sleep(10)