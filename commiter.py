__author__ = 'cltanuki'
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
        TwitterUser.create_table()
        self.get_profile_links()
        if len(self.profile_list) < 1:
            sleep(10)
            self.main()
        with db.transaction():
            for data_dict in self.profile_list:
                TwitterUser.create(**data_dict)