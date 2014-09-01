__author__ = 'cltanuki'
import requests
from bs4 import BeautifulSoup


domain = 'https://twitter.com'


def get_links():
    page = requests.get('https://twitter.com/i/directory/profiles')
    soup = BeautifulSoup(page.text)
    links_div = soup.find('div', class_='top-levels')
    links = [domain + link['href'] for link in links_div.find_all('a')]
    links.append(domain + '/i/directory/profiles/a')
    return links


def get_profile_links(links):
    level = 3
    last_level = 4
    dir_links = {}
    dir_links[last_level] = links
    print(dir_links)
    profile_links = {}
    while level != 0:
        dir_links[level] = []
        links = dir_links.get(last_level)
        print('links: ', links)
        for link in links:
            print('link: ', link)
            page = requests.get(link)
            soup = BeautifulSoup(page.text)
            links_div = soup.find('div', class_='directory-page').find('div', class_='row')
            links = [domain + link['href'] for link in links_div.find_all('a')]
            dir_links[level] += links
        level -= 1
        last_level -= 1
    print(type(dir_links))

get_profile_links(get_links())
# for link in links:
#     print(link)