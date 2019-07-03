#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup


class MusicInfo:
    def __init__(self):
        self.title = ''
        self.url = ''
        self.intro = ''
        self.tags = ''
        self.comment = ''
        self.rating_date = ''
        self.rating = ''

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


class MusicReview:
    def __init__(self):
        self.title = ''
        self.url = ''
        self.id = ''
        self.content = ''

    @classmethod
    def parse(cls, item):
        instance = cls()
        instance.title = item.select('h3')[0].text.strip()
        instance.url = item.select('h3 > a')[0]['href']
        m = re.search(r'\d+', instance.url)
        if m:
            instance.id = m.group(0)
        return instance

    def __str__(self):
        s = []
        for k in self.__dict__:
            s.append("{key}={value}".format(key=k, value=self.__dict__.get(k)))
        return ', '.join(s)

    def __repr__(self):
        return self.__str__()


class MusicExport:
    """
    遍历网页的问题可能被豆瓣反爬虫机制伤及，如果能够直接从接口 dump 数据就比较快
    """
    BASE_URL = 'https://music.douban.com/people/{}'
    WATCHED = 'collect'
    WISH = 'wish'
    DOING = 'do'

    def __init__(self, nickname):
        self.user_url = MusicExport.BASE_URL.format(nickname)

    def get_musics(self, path=WATCHED):
        """
        https://music.douban.com/people/einverne/collect
        第 1 页 https://music.douban.com/people/einverne/collect?start=0&sort=time&rating=all&filter=all&mode=grid
        第 2 页 https://music.douban.com/people/einverne/collect?start=15&sort=time&rating=all&filter=all&mode=grid
        第 3 页 https://music.douban.com/people/einverne/collect?start=30&sort=time&rating=all&filter=all&mode=grid
        ...
        https://music.douban.com/people/einverne/collect?start=60&sort=time&rating=all&filter=all&mode=grid
        """
        start = 0
        while True:
            item_list = self.__get_music_list(path, start)
            step = len(item_list)
            if step == 0:
                break
            for item in item_list:
                yield MusicInfo.parse(item)
            if step < 30:
                break
            start += step

    def __get_music_list(self, path='collect', start=0):
        url = self.user_url + '/' + path
        r = requests.get(url, params={
            'start': start,
            'sort': 'time',
            'rating': 'all',
            'filter': 'all',
            'mode': 'list'
        }, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': url + '?start=0&sort=time&rating=all&filter=all&mode=grid',
            'Host': 'music.douban.com'
        })
        # res = brotli.decompress(r.content)
        soup = BeautifulSoup(r.text, 'html.parser')
        item_list = soup.select('.item')
        return item_list

    def get_watched(self):
        return self.get_musics()

    def get_wish(self):
        """https://music.douban.com/people/einverne/wish"""
        return self.get_musics(self.WISH)

    def get_doing(self):
        """https://music.douban.com/people/einverne/do"""
        return self.get_musics(self.DOING)

    def get_reviews(self):
        """
        Get one's all music reviews

        https://music.douban.com/people/einverne/reviews?start=0
        https://music.douban.com/j/review/10000057/fullinfo?show_works=False
        """
        start = 0
        while True:
            reviews_list = self.__get_reviews_list(start)
            step = len(reviews_list)
            if step == 0:
                break
            for review in reviews_list:
                r = MusicReview.parse(review)
                content = self.get_review_content(r.id)
                bs = BeautifulSoup(content, 'html.parser')
                r.content = bs.text
                yield r
            start += step

    def __get_reviews_list(self, start=0):
        url = self.user_url + '/reviews'
        r = requests.get(url, params={
            'start': start
        }, headers={
            'Host': 'music.douban.com',
            'Referer': self.user_url + '/reviews?start=10',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.select('.tlst')

    def get_doulist(self):
        """
        创建的豆列 https://www.douban.com/people/einverne/doulists/all?start=20&tag=
        关注的豆列 https://www.douban.com/people/einverne/doulists/collect?start=20
        """
        pass

    def get_review_content(self, id='10124597'):
        """
        Get all review content by pass ID, return the content str
            https://music.douban.com/j/review/10124597/fullinfo?show_works=False
        :param id:
        :return:
        """
        url = "https://music.douban.com/j/review/{}/fullinfo?show_works=False".format(id)
        r = requests.get(url, headers={
            'Host': 'music.douban.com',
            'Referer': self.user_url + '/reviews?start=10',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        })
        return r.json()['html']


if __name__ == '__main__':
    m = MusicExport('einverne')
    # l = m.get_musics()
    # for item in l:
    #     print(item)
    wishes = m.get_wish()
    for wish in wishes:
        print(wish)
    reviews = m.get_reviews()
    for r in reviews:
        print(r)
