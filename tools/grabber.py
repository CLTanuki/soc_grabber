__author__ = 'cltanuki'
import requests
import os
import signal
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from requests.exceptions import ConnectionError as ReqErr
from requests.packages.urllib3.exceptions import MaxRetryError
from db_work.models import Proxy


class LinkGrabber():

    def __init__(self, domain, start_url, dir_str, dir_links, profile_links,
                 start_link, find_attrs, proxy_usage, secret_str):
        self.domain = domain
        self.start_url = start_url
        self.dir_links_queue = dir_links
        self.profile_links_queue = profile_links
        self.dir_links = []
        self.dir_links.append(start_link)
        self.dir_str = dir_str
        self.find_attrs = find_attrs
        self.proxies = {'http': ''}
        self.secret_str = secret_str
        self.profile_counter = 0
        self.proxy_usage = proxy_usage
        signal.signal(signal.SIGALRM, self.handler)

    def handler(self, signum, frame):
        raise ConnectionError

    def change_proxies(self):
        proxy_list = [proxy.body for proxy in Proxy.select().where(Proxy.level == True)]
        self.proxies['https'] = 'http://' + str(proxy_list[randint(0, len(proxy_list) - 1)])

    def delete_proxy(self):
        proxy = Proxy.select().where(Proxy.body == self.proxies['https'][7:])
        proxy.level = False
        proxy.save()

    def grab_cycle(self, link):
        url = self.domain + self.secret_str + link
        page = requests.get(url, proxies=self.proxies).text
        soup = BeautifulSoup(page)
        links_div = soup.find('div', **self.find_attrs)
        print(links_div)
        for link in links_div.find_all('a'):
            if link['href'] == self.dir_str or 'articles' in link['href']:
                pass
            if self.dir_str in link['href']:
                self.dir_links_queue.put(link['href'])
            else:
                profile_data = {'url': link['href']}
                self.profile_links_queue.put(profile_data)

    def grab_links(self, link):
        if self.proxy_usage:
            self.change_proxies()
            try:
                signal.alarm(100)
                self.grab_cycle(link)
            except (ConnectionError, ConnectionRefusedError, MaxRetryError, ConnectionResetError,
                    AttributeError, ReqErr):
                self.grab_links(link)
            except (TypeError, IndexError):
                sleep(1)
                self.grab_links(link)
        else:
            try:
                self.grab_cycle(link)
            except AttributeError:
                self.dir_links_queue.put(link)

    def get_dir_links(self):
        while not self.dir_links_queue.empty():
            self.dir_links.append(self.dir_links_queue.get())

    def iteration(self):
        self.get_dir_links()
        if self.dir_links:
            for link in self.dir_links:
                self.grab_links(link)
            self.dir_links = []
        else:
            sleep(10)

    def main(self):
        while True:
            self.iteration()
