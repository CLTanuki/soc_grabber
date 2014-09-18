__author__ = 'cltanuki'
import signal
from requests import get, post
import socket
from bs4 import BeautifulSoup
from db_work.models import meta_db, Proxy
from peewee import IntegrityError


class ProxyGrabber():
    def __init__(self, collect_mode=False):
        self.proxy_dict = {"http": "", "https": ""}
        self.port_dict = {'3128': '1', '8080': '2', '80': '3'}
        self.proxies = []
        self.collect_mode = collect_mode

    def request_proxy(self, p_type):
        url = 'http://spys.ru/en/https-ssl-proxy/'
        data = {'xpp': '3', 'xf1': '0', 'xf4': p_type}
        resp = post(url, data=data).text
        return resp

    def test_connection(self, proxy):
        socket.timeout(30)
        try:
            http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            http.connect((proxy[0], int(proxy[1])))
            request = "GET /search?output=search&q=habrahabr HTTP/1.1\r\n"
            request += "Host: https://www.google.com\r\n"
            http.send(request.encode("utf-8", "strict"))
            http.recv(65535)
            return True
        except socket.error:
            return False

    def check(self):
        print('Begin checking')
        for proxy in Proxy.select().where(Proxy.level >> None):
            proxy_body = proxy.body.split(':')
            speed = self.test_connection(proxy_body)
            proxy.level = speed
            proxy.save()
        print('Done checking')
        Proxy.delete().where(Proxy.level == False)

    def commit(self):
        meta_db.connect()
        meta_db.create_table(Proxy, safe=True)
        with meta_db.transaction():
            #Proxy.insert_many(self.proxies).execute()
            for data_dict in self.proxies:
                try:
                    Proxy.create(**data_dict)
                except IntegrityError:
                    pass
        self.proxies = []

    def collect(self):
        print('Begin collecting')
        for k, v in self.port_dict.items():
            port = k
            html = self.request_proxy(v)
            rip = BeautifulSoup(html)
            table_body = rip.find("body")
            trs = table_body.find_all("table")[2].find_all("tr", {"onmouseover": "this.style.background='#002424'"})
            for tr in trs:
                tds = tr.find_all('td')
                raw_proxy_td = tds[0].find('font', class_='spy14').text
                ip = raw_proxy_td.partition('14">')[0].rpartition('d')[0]
                proxy_body = ip + ':' + port
                self.proxies.append({'body': proxy_body})

    def main(self):
        while True:
            self.collect()
            self.commit()
            if self.collect_mode:
                break
            self.check()


if __name__ == '__main__':
    grabber = ProxyGrabber()
    grabber.main()