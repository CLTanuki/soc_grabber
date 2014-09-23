#!/usr/bin/python3.4
__author__ = 'cltanuki'
from multiprocessing import Process, Queue
from datetime import datetime

from tools.serv import app
from tools.grabber import LinkGrabber
from proxist import ProxyGrabber
from db_work.profile_commiter import Commiter
from db_work.models import TwitterUser, VkUser


class LinkWorker():

    def __init__(self, domain, start_url, dir_str, find_attrs, table, secret_str=None, proxy_usage=False):
        self.domain = domain
        self.start_url = start_url
        self.dir_str = dir_str
        self.jobs = []
        self.find_attrs = find_attrs
        self.dir_links = Queue()
        self.start_links = []
        self.profile_links = Queue()
        self.table = table
        self.proxy_usage = proxy_usage
        self.proxies = {}
        self.secret_str = secret_str if secret_str else ''
        self.counter = 30

    def get_start_links(self):
        raise NotImplementedError

    def get_dir_links(self):
        while self.counter:
            self.start_links.append(self.dir_links.get())
            self.counter -= 1

    def set_workers(self):
        self.get_start_links()
        self.get_dir_links()
        self.jobs.append(Process(target=Commiter(profile_queue=self.profile_links,
                                                 table=self.table).main, args=()))
        print(len(self.start_links))
        for link in self.start_links:
            self.jobs.append(Process(target=LinkGrabber(domain=self.domain, start_url=self.start_url,
                                                        dir_str=self.dir_str, dir_links=self.dir_links,
                                                        profile_links=self.profile_links, start_link=link,
                                                        find_attrs=self.find_attrs, proxy_usage=self.proxy_usage,
                                                        secret_str=self.secret_str).main, args=()))

    def start_workers(self):
        self.set_workers()
        for job in self.jobs:
            job.start()
        for job in self.jobs:
            job.join()


class TwitterWorker(LinkWorker):

    def get_start_links(self):
        LinkGrabber(domain=self.domain, start_url=self.start_url, dir_str=self.dir_str,
                    dir_links=self.dir_links, profile_links=self.profile_links, start_link=self.start_url,
                    find_attrs={'class_': 'top-levels'}, secret_str='', proxy_usage=False).iteration()


class VKWorker(LinkWorker):

    def get_start_links(self):
        LinkGrabber(domain=self.domain, start_url=self.start_url, dir_str=self.dir_str,
                    dir_links=self.dir_links, profile_links=self.profile_links, start_link=self.start_url,
                    find_attrs=self.find_attrs, proxy_usage=False, secret_str='/').iteration()


if __name__ == '__main__':
    print(datetime.now())
    jobs = []
    ProxyGrabber(collect_mode=True).main()
    jobs.append(Process(target=app.run))
    jobs.append(Process(target=ProxyGrabber().main, args=()))
    jobs.append(Process(target=TwitterWorker(domain='https://twitter.com', dir_str='directory',
                                             start_url='/i/directory/profiles', find_attrs={'class_': 'row'},
                                             table=TwitterUser, proxy_usage=False).start_workers))
    jobs.append(Process(target=VKWorker(domain='https://vk.com', dir_str='catalog.php', start_url='catalog.php',
                                        find_attrs={'id': 'wrap1'}, table=VkUser, secret_str='/').start_workers))
    for job in jobs:
        job.start()