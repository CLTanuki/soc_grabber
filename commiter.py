__author__ = 'cltanuki'
from os import path
from time import sleep
from models import db, TwitterUser


class Commiter():

    def __init__(self, profile_queue):
        self.profile_queue = profile_queue
        self.profile_list = []

    def get_profile_links(self):
        while not self.profile_queue.empty():
            self.profile_list.append(self.profile_queue.get())

    def main(self):
        if not path.isfile('people.db'):
            TwitterUser.create_table()
        self.get_profile_links()
        if self.profile_list:
            with db.transaction():
                print(self.profile_list)
                for data_dict in self.profile_list:
                    print(data_dict)
                    TwitterUser.create(**data_dict)
        else:
            sleep(10)
            self.main()