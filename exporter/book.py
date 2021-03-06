#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from exporter import *


class BookInfo(object):
    def __init__(self):
        self.title = ''
        self.url = ''
        self.intro = ''
        self.tags = ''
        self.comment = ''
        self.rating = ''
        self.rating_date = ''

    @classmethod
    def parse(cls, item):
        instance = cls()
        instance.title = item.select('.title a')[0].text.strip()
        instance.url = item.select('.title a')[0]['href']
        instance.intro = item.select('.intro')[0].text.strip()
        instance.rating_date = item.select('.date')[0].text.strip()
        if len(item.select('.date span')) > 0:
            instance.rating = item.select('.date span')[0]['class'][0][6]
        if len(item.select('.tags')) > 0:
            instance.tags = item.select('.tags')[0].text
        if len(item.select('.comment')) > 0:
            instance.comment = item.select('.comment')[0].text.strip()
        return instance

    def __str__(self):
        s = []
        for k in self.__dict__:
            s.append("{key}={value}".format(key=k, value=self.__dict__.get(k)))
        return ', '.join(s)

    def __repr__(self):
        return self.__str__()


class BookReview(BaseReview):

    def parse(self, item):
        self.title = item.select('h3')[0].text.strip()
        self.url = item.select('h3 > a')[0]['href']
        self.id = r0(r'\d+', self.url)
        return self


class BookExport(BaseExporter):
    BASE_URL = 'https://book.douban.com/people/{}'

    def __init__(self, nickname):
        self.user_url = BookExport.BASE_URL.format(nickname)

    def get_books(self, path=COLLECT):
        start = 0
        while True:
            item_list = self.__get_book_list(path, start)
            step = len(item_list)
            if step == 0:
                break
            for item in item_list:
                yield BookInfo.parse(item)
            if step < 30:
                break
            start += step

    def __get_book_list(self, path=COLLECT, start=0):
        url = self.user_url + '/' + path
        r = requests.get(url, params={
            'start': start,
            'sort': 'time',
            'rating': 'all',
            'filter': 'all',
            'mode': 'list'
        }, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': url + '?start=0&sort=time&rating=all&filter=all&mode=list',
            'Host': 'book.douban.com'
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.select('.item')

    def get_read(self):
        return self.get_books(COLLECT)

    def get_wish(self):
        return self.get_books(WISH)

    def get_reading(self):
        return self.get_books(DOING)

    def get_reviews(self):
        start = 0
        while True:
            reviews_list = self.__get_reviews_list(start)
            step = len(reviews_list)
            if step == 0:
                break
            for review in reviews_list:
                r = BookReview()
                r.parse(review)
                content = self.get_review_content(r.id)
                r.update(content)
                yield r
            start += step

    def __get_reviews_list(self, start=0):
        url = self.user_url + '/reviews'
        r = requests.get(url, params={
            'start': start
        }, headers={
            'Host': 'book.douban.com',
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.select('.tlst')


if __name__ == '__main__':
    b = BookExport('einverne')
    for review in b.get_reviews():
        print(review)
    # for book in b.get_books():
    #     print(book.title)
