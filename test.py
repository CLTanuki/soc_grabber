__author__ = 'cltanuki'
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
from grabber import LinkGrabber


class Worker():

    def __init__(self, domain, start_url, dir_str):
        self.domain = domain
        self.start_url = start_url
        self.dir_links = Queue()
        self.profile_links = Queue()
        self.dir_str = dir_str
        self.jobs = []

    def _get_start_links(self):
        page = requests.get(self.domain + self.start_url)
        soup = BeautifulSoup(page.text)
        links_div = soup.find('div', class_='top-levels')
        links = [link['href'] for link in links_div.find_all('a')]
        links.append('/i/directory/profiles/a')
        return links

    def start_grabber(self, link):
        grabber = LinkGrabber(domain=self.domain, start_url=self.start_url, dir_str=self.dir_str,
                              dir_links=self.dir_links, profile_links=self.profile_links, start_link=link)
        grabber.main()

    def set_workers(self):
        links = self._get_start_links()
        print(links)
        for link in links:
            self.jobs.append(Process(target=self.start_grabber, args=(link, )))

    def start_workers(self):
        self.set_workers()
        for job in self.jobs:
            job.start()
        print(u"All workers were started")


if __name__ == '__main__':
    grabber = Worker(domain='https://twitter.com', dir_str='directory',
                     start_url='/i/directory/profiles')
    grabber.start_workers()

# for link in links:
#     print(link)