#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import urllib.parse

import requests
from bs4 import BeautifulSoup, NavigableString

from utils.logutil import  log

SEARCH_URL = 'https://movie.douban.com/j/subject_suggest?q='
PAGE_URL = 'https://movie.douban.com/subject/%s/'




class Movie:
    def __init__(self):
        self.id = ''
        self.title = ''
        self.score = 0
        self.director = ''
        self.actor = ''
        self.year = ''
        self.sub_title = ''

    def __str__(self):
        text = '===============   Douban Movie   ===============\n' + \
               'Title: ' + self.title + '\n' + \
               'Score: ' + str(self.score) + '\n' + \
               'Year: ' + self.year + '\n' + \
               'Director: ' + self.director + '\n' + \
               'Actors: ' + self.actor + '\n' + \
               '================================================'
        return text.encode('utf-8')


def search(query_word):
    query_word = urllib.parse.quote(query_word)
    url = SEARCH_URL + query_word
    r = requests.get(url)
    if r.status_code != 200:
        return

    data = r.text.encode('utf-8')
    items = json.loads(data)
    if len(items) == 0:
        return
    movies = []
    for item in items:
        if item['type'] != 'movie':
            continue
        movie = Movie()
        movie.id = item['id']
        movie.title = item['title']
        movie.year = item['year']
        movie.sub_title = item['sub_title']
        movies.append(movie)
    return movies


def parse(movie):
    url = PAGE_URL % movie.id
    log.debug(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    movie.score = soup.find('strong', 'rating_num').text
    info = soup.find('div', {'id': 'info'})
    for linebreak in info.find_all('br'):
        linebreak.extract()
    for span in info.contents:
        if isinstance(span, NavigableString):
            continue
        if span.contents[0]:
            if span.contents[0].string == u'导演':
                if isinstance(span.contents[1], NavigableString):
                    movie.director = span.contents[2].text
            elif span.contents[0].string == u'主演':
                if isinstance(span.contents[1], NavigableString):
                    movie.actor = span.contents[2].text
    print(movie)


def get_movie(text):
    movies = search(text)
    if movies and len(movies):
        parse(movies[0])
    else:
        print('cound not find movie: ' + text)


if __name__ == '__main__':
    get_movie("zootopia")