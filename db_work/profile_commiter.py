__author__ = 'cltanuki'
from os import path
from time import sleep
from db_work.models import soc_db


class Commiter():

    def __init__(self, profile_queue, table):
        self.profile_queue = profile_queue
        self.profile_list = []
        self.table = table

    def get_profile_links(self):
        while not self.profile_queue.empty():
            self.profile_list.append(self.profile_queue.get())

    def main(self):
        #print('Commiter started.')
        soc_db.connect()
        soc_db.create_table(self.table, safe=True)
        while True:
            self.get_profile_links()
            if not self.profile_list:
                sleep(1)
            else:
                with soc_db.transaction():
                    for data_dict in self.profile_list:
                        self.table.create(**data_dict)
                print('Commited: ' + str(len(self.profile_list)))
                self.profile_list = []