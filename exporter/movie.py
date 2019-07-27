#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup

from exporter import r0, BaseExporter, BaseReview

"""
<li class="item" id="list27617348">
<div class="item-show">
<div class="title">
<a href="https://movie.douban.com/subject/27617348/">
                门锁 / 도어락
            </a>
</div>
<div class="date">
<span class="rating4-t"></span>  
        2019-03-16
        </div>
</div>
<div class="hide" id="grid27617348">
<div class="grid-date">
<span class="intro">2018-12-05(韩国) / 孔晓振 / 金叡园 / 金圣武 / 赵福来 / 李家燮 / 李天熙 / 金在华 / 金光奎 / 韩智恩 / 车烨 / 裴明真 / 郑钟宇 / 李钟求 / 尹钟硕 / 李相熹 / 韩国 / 李权 / 102分钟 / 门锁 / 悬疑 / 惊悚 / 朴正熙 Jeong-hee Park / 李权 Kwon Lee / 阿尔贝托·马里尼 Alberto Marini / 韩语</span><br/>
<span class="tags">标签: 犯罪 惊悚悬疑 剧情 悬疑 韩国 恐怖 2018 惊悚 惊悚片</span>
</div>
</div>
</li>
"""


class MovieInfo:
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


class MovieReview(BaseReview):

    def parse(self, item):
        self.title = item.select('h3')[0].text.strip()
        self.url = item.select('h3 > a')[0]['href']
        self.id = r0(r'\d+', self.url)
        return self


class MovieExport(BaseExporter):
    """
    遍历网页的问题可能被豆瓣反爬虫机制伤及，如果能够直接从接口 dump 数据就比较快
    """
    BASE_URL = 'https://movie.douban.com/people/{}'
    WATCHED = 'collect'
    WISH = 'wish'
    DOING = 'do'

    def __init__(self, nickname):
        self.user_url = MovieExport.BASE_URL.format(nickname)

    def get_movies(self, path=WATCHED):
        """
        https://movie.douban.com/people/einverne/collect
        第 1 页 https://movie.douban.com/people/einverne/collect?start=0&sort=time&rating=all&filter=all&mode=grid
        第 2 页 https://movie.douban.com/people/einverne/collect?start=15&sort=time&rating=all&filter=all&mode=grid
        第 3 页 https://movie.douban.com/people/einverne/collect?start=30&sort=time&rating=all&filter=all&mode=grid
        ...
        https://movie.douban.com/people/einverne/collect?start=60&sort=time&rating=all&filter=all&mode=grid
        """
        start = 0
        while True:
            item_list = self.__get_movie_list(path, start)
            step = len(item_list)
            if step == 0:
                break
            for item in item_list:
                yield MovieInfo.parse(item)
            if step < 30:
                break
            start += step

    def __get_movie_list(self, path='collect', start=0):
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
            'Host': 'movie.douban.com'
        })
        # res = brotli.decompress(r.content)
        soup = BeautifulSoup(r.text, 'html.parser')
        item_list = soup.select('.item')
        return item_list

    def get_watched(self):
        return self.get_movies()

    def get_wish(self):
        """https://movie.douban.com/people/einverne/wish"""
        return self.get_movies(self.WISH)

    def get_doing(self):
        """https://movie.douban.com/people/einverne/do"""
        return self.get_movies(self.DOING)

    def get_reviews(self):
        """
        Get one's all movie reviews

        https://movie.douban.com/people/einverne/reviews?start=0
        https://movie.douban.com/j/review/10000057/fullinfo?show_works=False
        """
        start = 0
        while True:
            reviews_list = self.__get_reviews_list(start)
            step = len(reviews_list)
            if step == 0:
                break
            for review in reviews_list:
                r = MovieReview()
                r.parse(review)
                raw_content = self.get_review_content(r.id)
                r.update(raw_content)
                yield r
            start += step

    def __get_reviews_list(self, start=0):
        url = self.user_url + '/reviews'
        r = requests.get(url, params={
            'start': start
        }, headers={
            'Host': 'movie.douban.com',
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


if __name__ == '__main__':
    m = MovieExport('einverne')
    # l = m.get_movies()
    # for item in l:
    #     print(item)
    # wishes = m.get_wish()
    # for wish in wishes:
    #     print(wish)
    reviews = m.get_reviews()
    for r in reviews:
        print(r)
