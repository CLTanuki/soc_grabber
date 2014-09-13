import re
from requests import get, ConnectionError
from os import path
from models import meta_db, Proxy
from bs4 import BeautifulSoup


class ProxyGrabber():
    def __init__(self):
        self.proxy_dict = {"http": "", "https": ""}
        self.test_addr_part = '://www.google.com'
        self.url = ''


    def request_proxy(self):
        url = 'http://proxylist.hidemyass.com'
        resp = get(url).text
        return resp


    def test_connection(self, protocol):
        try:
            addr = protocol.lower() + self.test_addr_part
            get(addr, proxies=self.proxy_dict).elapsed.total_seconds()
            return True
        except ConnectionError:
            return False


    def get_none_style(self, entry):
         # find all .XXX{display:XXXXX} styles
        temp = re.findall("\.(.+){display:(.+)}", entry)
        # will be filled with styles of display:none (MUST be initialized with display:none)
        none = ["display:none"]
        for s in temp:
            if "none" in s[1]:
                none.append(s[0])
        return none


    def get_entries(self, dest, table, pattern, special=False):
        """
            dest: where the values will be stored
            table: where to search
            pattern: what to search for
            special: should be set True if a value is located in </smthg>XXXX
        """

        end = 0
        temp = table
        while True:
            result = re.search(pattern, temp)
            if result:
                if special:  # if format is </smthg>XXXX
                    dest += [("inline", result.group(1), result.start()+end)]
                else:
                    dest += [(result.group(1), result.group(2), result.start()+end)]
                end += result.end()
                temp = temp[result.end():]
            else:
                break


    def get_ip(self, table, nones):
        table = sorted(table, key=lambda n: n[2])  # sort by position (third element)
        ip = ""
        for element in table:
            if element[0] not in nones:
                ip += element[1]
        return ip


    def commit(self, proxies):
        if not path.isfile('meta.db'):
                meta_db.connect()
                meta_db.create_table(Proxy)
        with meta_db.transaction():
            Proxy.insert_many(proxies).execute()


    def main(self):

        # Request page
        html = self.request_proxy()
        rip = BeautifulSoup(html)
        table_body = rip.find("table", {"id": "listable"}).find("tbody")

        # browse all proxy entries to extract data
        proxies = []
        for tr in table_body.find_all('tr'):
            tds = tr.find_all('td')
            # find the end of the proxy's entry
            port = tds[2].text.strip()
            protocol = tds[6].text

            # will be filled with styles of display:none
            none = self.get_none_style(tds[1].text)
            # git rid of .XXXX{display:XXXXXXX}
            proxy_td = str(tds[1])
            proxy = re.search("</style>(.+)</span></td>", proxy_td).group(1)
            # list of span's & </div>[0-9.]+ values and it's position
            table = []

            #==============================================
            # find <span ...="XXX">XXX</span>
            self.get_entries(table, proxy, '<span .+?="(.+?)">(.+?)</span>')
            #==============================================
            # find <span...>...</span>XXX<span...>
            #==============================================
            self.get_entries(table, proxy, '</span>([0-9.]+)', True)
            #==============================================
            # find <div...>...</div>XXX<span...>
            #==============================================
            self.get_entries(table, proxy, '</div>([0-9.]+)', True)
            #==============================================
            # special:XXX<span... at the beginning
            #==============================================
            result = re.match('([0-9.]+)', proxy)
            if result:
                table += [("inline", result.group(1), result.start())]

            ip = self.get_ip(table, none)
            if 'socks' in protocol:
                continue
            proxy_body = ip + ':' + port
            self.proxy_dict[protocol.lower()] = proxy_body
            print("%-15s|%-6s|%-6s" % (ip, port, protocol))
            speed = self.test_connection(protocol)

            if speed:
                print('approoved... seeking...')
                proxies.append({'type': protocol, 'body': proxy_body})
            else:
                print('bad... seeking...')

        self.commit(proxies)
        print('Commited: ' + str(len(proxies)))


if __name__ == '__main__':
    grabber = ProxyGrabber()
    grabber.main()