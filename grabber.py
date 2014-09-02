__author__ = 'cltanuki'
import requests
import os
from bs4 import BeautifulSoup


class LinkGrabber():

    def __init__(self, domain, start_url, dir_str, dir_links, profile_links, start_link):
        self.domain = domain
        self.start_url = start_url
        self.dir_links_queue = dir_links
        self.profile_links_queue = profile_links
        self.dir_links = []
        self.dir_links.append(start_link)
        self.dir_str = dir_str

    def grab_links(self, link):
        page = requests.get(self.domain + link)
        soup = BeautifulSoup(page.text)
        links_div = soup.find('div', class_='directory-page').find('div', class_='row')
        links = [link['href'] for link in links_div.find_all('a')]
        for link in links:
            if self.dir_str in link:
                self.dir_links_queue.put(link)
            elif len(link) < 30:
                self.profile_links_queue.put(link)
            else:
                print(link)
                os._exit()

    def get_dir_links(self):
        while not self.dir_links_queue.empty():
            self.dir_links.append(self.dir_links_queue.get())

    def main(self):
        while True:
            self.get_dir_links()
            print(self.dir_links)
            for link in self.dir_links:
                self.grab_links(link)