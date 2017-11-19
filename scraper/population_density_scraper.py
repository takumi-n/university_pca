# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import json


def get_city_url(university_url):
    html = urllib2.urlopen(university_url)
    soup = BeautifulSoup(html, "html.parser")
    ths = soup.find_all('th')
    for th in ths:
        if th.text == u'本部所在地':
            links = th.find_next_sibling('td').find_all('a')
            for l in links:
                if re.search(u'(市|区|町|村)$', l.text):
                    city_url = 'https://ja.wikipedia.org' +  l.get('href')
                    return city_url
    return None


def get_population_density(city_url):
    html = urllib2.urlopen(city_url)
    soup = BeautifulSoup(html, "html.parser")
    ths = soup.find_all('th')
    for th in ths:
        if th.text == u'人口密度':
            population_density_str = th.find_next_sibling('td').text
            return population_density_str.replace(',', '').split(u'人')[0]
    return None


def main():
    master_file = '../data/university_name_master.csv'
    f = open(master_file, 'r')
    lines = f.readlines()
    lines = map(lambda x: x.rstrip(), lines)
    f.close()
    for l in lines:
        university_name = l.split(',')[0]
        university_name = unicode(university_name, 'utf-8')
        university_url = 'https://ja.wikipedia.org/wiki/%s' %(urllib.quote(university_name.encode('utf-8')))
        city_url = get_city_url(university_url)
        population_density = get_population_density(city_url)
        print population_density


if __name__ == '__main__':
    main()
