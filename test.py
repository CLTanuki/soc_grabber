__author__ = 'cltanuki'
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue


class Grabber():

    def __init__(self, domain, start_url):
        self.domain = domain
        self.start_url = start_url
        self.dir_links = Queue()
        self.profile_links = Queue()

    def get_start_links(self):
        page = requests.get(self.start_url)
        soup = BeautifulSoup(page.text)
        links_div = soup.find('div', class_='top-levels')
        links = [self.domain + link['href'] for link in links_div.find_all('a')]
        links.append(self.domain + '/i/directory/profiles/a')
        return links

    def grab_links(self, link):
        page = requests.get(link)
        soup = BeautifulSoup(page.text)
        links_div = soup.find('div', class_='directory-page').find('div', class_='row')
        links = [self.domain + link['href'] for link in links_div.find_all('a')]

    def main(self):
        self.grab_links(self.get_start_links())


if __name__ == '__main__':
    grabber = Grabber(domain='https://twitter.com', start_url='https://twitter.com/i/directory/profiles')
    grabber.main()

# for link in links:
#     print(link)