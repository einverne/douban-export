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


class StatusExport:
    """
    遍历网页的问题可能被豆瓣反爬虫机制伤及，如果能够直接从接口 dump 数据就比较快
    """
    BASE_URL = 'https://www.douban.com/people/{}/statuses'

    def __init__(self, nickname):
        self.user_url = StatusExport.BASE_URL.format(nickname)

    def get_status(self):
        """
        https://music.douban.com/people/einverne/collect
        第 1 页 https://music.douban.com/people/einverne/collect?start=0&sort=time&rating=all&filter=all&mode=grid
        第 2 页 https://music.douban.com/people/einverne/collect?start=15&sort=time&rating=all&filter=all&mode=grid
        第 3 页 https://music.douban.com/people/einverne/collect?start=30&sort=time&rating=all&filter=all&mode=grid
        ...
        https://music.douban.com/people/einverne/collect?start=60&sort=time&rating=all&filter=all&mode=grid
        """
        start = 1
        while True:
            item_list = self.__get_status_by_page(start)
            step = len(item_list)
            if step == 0:
                break
            for item in item_list:
                yield MusicInfo.parse(item)
            if step < 30:
                break
            start += step

    def __get_status_by_page(self, page_num=1):
        url = self.user_url
        r = requests.get(url, params={
            'p': page_num,
        }, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': url,
            'Host': 'www.douban.com'
        })
        # res = brotli.decompress(r.content)
        soup = BeautifulSoup(r.text, 'html.parser')
        item_list = soup.select('.new-status status-wrapper')
        return item_list

    def get_watched(self):
        return self.get_status()

    def get_wish(self):
        """https://music.douban.com/people/einverne/wish"""
        return self.get_status(self.WISH)

    def get_doing(self):
        """https://music.douban.com/people/einverne/do"""
        return self.get_status(self.DOING)



if __name__ == '__main__':
    m = StatusExport('einverne')
    l = m.get_status()
    for item in l:
        print(item)
    wishes = m.get_wish()
    for wish in wishes:
        print(wish)
    reviews = m.get_reviews()
    for r in reviews:
        print(r)
