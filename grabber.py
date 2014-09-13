__author__ = 'cltanuki'
import requests
import os
from bs4 import BeautifulSoup
from random import randint
from time import sleep


class LinkGrabber():

    def __init__(self, domain, start_url, dir_str, dir_links, profile_links, start_link,
                 first_class, second_class, proxy):
        self.domain = domain
        self.start_url = start_url
        self.dir_links_queue = dir_links
        self.profile_links_queue = profile_links
        self.dir_links = []
        self.dir_links.append(start_link)
        self.dir_str = dir_str
        self.first_class = first_class
        self.second_class = second_class
        self.proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
        self.counter = 0

    def grab_links(self, link):
        page = requests.get(self.domain + link, proxies=self.proxies)
        soup = BeautifulSoup(page.text)
        links_div = soup.find('div', class_=self.first_class).find('div', class_=self.second_class)
        for link in links_div.find_all('a'):
            if self.dir_str in link['href']:
                self.dir_links_queue.put(link['href'])
            else:
                profile_data = {'screenname': link.text, 'url': link['href']}
                self.profile_links_queue.put(profile_data)

    def get_dir_links(self):
        while not self.dir_links_queue.empty():
            self.dir_links.append(self.dir_links_queue.get())

    def main(self):
        while True:
            self.get_dir_links()
            if self.dir_links:
                for link in self.dir_links:
                    self.grab_links(link)
                    self.counter += 1
                self.dir_links = []
            else:
                sleep(10)