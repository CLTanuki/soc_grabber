__author__ = 'cltanuki'
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue
from grabber import LinkGrabber
from commiter import Commiter
from random import randint


class Worker():

    def __init__(self, domain, start_url, dir_str, first_class, second_class):
        self.domain = domain
        self.start_url = start_url
        self.dir_links = Queue()
        self.profile_links = Queue()
        self.dir_str = dir_str
        self.jobs = []
        self.first_class = first_class
        self.second_class = second_class
        self.proxies = ['162.208.49.45:7808', '217.112.131.63:8089', '185.28.22.119:3128', '93.115.8.229:3127',
                        '62.210.56.250:8089', '62.210.56.250:3127', '62.244.31.16:8089', '162.208.49.45:8089',
                        '144.76.6.149:3128', '107.182.16.221:3127', '104.131.250.241:3128', '209.203.212.4:3128',
                        '74.50.126.248:8089', '74.50.126.249:8089', '162.213.152.3:8080', '90.183.26.65:80',
                        '192.3.10.101:3128', '74.50.126.249:3127', '62.64.13.25:3128', '74.124.13.189:3127',
                        '184.164.77.109:3127', '134.19.178.70:8089', '162.144.62.9:3128', '164.138.208.84:80',
                        '193.140.229.249:3128', '85.222.163.30:8080', '190.144.181.5:3128', '46.10.209.122:3128',
                        '198.148.112.46:3127', '92.51.245.87:3128', '23.239.23.47:3128', '104.143.14.183:3128',
                        '65.255.36.245:80', '41.208.68.52:8080', '184.164.77.109:8089', '223.202.68.83:3129',
                        '186.219.34.149:8080', '190.85.83.181:8080', '190.184.144.141:8080', '184.164.77.109:7808',
                        '213.108.200.39:3128', '118.97.134.114:80', '192.3.17.220:8080', '192.99.7.196:3128',
                        '201.234.226.82:8080', '153.122.27.122:3128', '190.102.151.231:3128', '193.227.161.211:8085',
                        '186.95.217.87:8080', '188.120.241.41:8080', '201.221.132.46:8080', '109.175.6.194:8080',
                        '195.154.91.100:3128', '190.128.191.202:8080', '221.146.243.236:3128', '200.84.65.231:8080',
                        '190.128.149.34:8080', '212.232.52.56:8080', '88.81.230.68:3128', '79.136.250.38:3128',
                        '157.7.204.218:3128', '110.93.215.117:8080', '219.94.254.206:8080', '80.241.220.123:3128',
                        '107.182.16.221:8089', '187.72.105.65:3128', '115.112.186.90:3128', '201.18.78.220:8080',
                        '221.146.243.48:3128', '187.33.48.162:8080', '86.125.59.121:3128', '46.32.18.121:8080',
                        '209.170.151.142:8089', '217.112.131.63:7808', '190.151.10.226:8080', '62.244.31.16:7808',
                        '185.49.15.25:3127', '80.91.178.237:3128', '188.241.141.112:7808', '162.216.155.136:7808',
                        '107.150.224.29:8080', '207.223.117.198:3128', '101.69.192.33:8080', '87.106.131.34:3128',
                        '188.241.141.112:8089', '61.247.188.66:8080', '186.92.143.82:8080', '188.241.141.112:3127',
                        '37.187.242.67:1234', '190.113.162.142:8080', '66.192.33.78:3128', '36.250.69.4:80',
                        '134.19.178.70:3127', '134.19.178.70:7808', '20.132.160.149:80', '107.182.16.221:7808',
                        '107.0.69.189:3128', '209.170.151.142:3127', '110.173.49.18:3128', '89.46.101.122:8089']

    def _get_start_links(self):
        page = requests.get(self.domain + self.start_url)
        soup = BeautifulSoup(page.text)
        links_div = soup.find('div', class_='top-levels')
        links = [link['href'] for link in links_div.find_all('a')]
        links.append('/i/directory/profiles/a')
        return links

    def start_grabber(self, link, proxy):
        grabber = LinkGrabber(domain=self.domain, start_url=self.start_url, dir_str=self.dir_str,
                              dir_links=self.dir_links, profile_links=self.profile_links, start_link=link,
                              first_class=self.first_class, second_class=self.second_class, proxy=proxy)
        grabber.main()

    def start_commiter(self):
        commiter = Commiter(profile_queue=self.profile_links)
        commiter.main()

    def set_workers(self):
        links = self._get_start_links()
        for link in links:
            proxy = self.proxies.pop(randint(0, len(self.proxies) - 1))
            self.jobs.append(Process(target=self.start_grabber, args=(link, proxy)))
        self.jobs.append(Process(target=self.start_commiter, args=()))

    def start_workers(self):
        self.set_workers()
        for job in self.jobs:
            job.start()
        print(u"All workers were started")


if __name__ == '__main__':
    grabber = Worker(domain='https://twitter.com', dir_str='directory', start_url='/i/directory/profiles',
                     first_class='directory-page', second_class='row')
    grabber.start_workers()