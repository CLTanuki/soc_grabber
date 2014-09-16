__author__ = 'cltanuki'
import requests
import os
import signal
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import MaxRetryError
from db_work import seeker, models


class ProxOut(Exception):
    pass


class LinkGrabber():

    def __init__(self, domain, start_url, dir_str, dir_links, profile_links,
                 start_link, css_class_str, proxy_usage, secret_str):
        self.domain = domain
        self.start_url = start_url
        self.dir_links_queue = dir_links
        self.profile_links_queue = profile_links
        self.dir_links = []
        self.dir_links.append(start_link)
        self.dir_str = dir_str
        self.css_class_str = css_class_str
        self.proxies = {'http': ''}
        self.secret_str = secret_str
        self.profile_counter = 0
        self.proxy_usage = proxy_usage

    def handler(self, signum, frame):
        raise ProxOut

    def change_proxies(self):
        proxy_list = [proxy.body for proxy in seeker.Seeker(models.Proxy).get()]
        print('s')
        self.proxies['https'] = 'https://' + str(proxy_list[randint(0, len(proxy_list) - 1)])

    def grab_cycle(self, link):
        url = self.domain + self.secret_str + link
        page = requests.get(url, proxies=self.proxies).text
        soup = BeautifulSoup(page)
        links_div = soup.find('div', class_=self.css_class_str)
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
            try:
                self.change_proxies()
                signal.alarm(90)
                try:
                    self.grab_cycle(link)
                except ProxOut:
                    print('smth')
                    self.change_proxies()
                    self.grab_links(link)
            except Exception:
                self.change_proxies()
                self.grab_links(link)
            except (ConnectionError, ProxOut, ConnectionRefusedError, MaxRetryError, ConnectionResetError, AttributeError):
                print('smth2')
                self.change_proxies()
                self.grab_links(link)
            except TypeError:
                sleep(1)
                self.grab_links(link)
        else:
            self.grab_cycle(link)

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
        signal.signal(signal.SIGALRM, self.handler)
        while True:
            self.iteration()
