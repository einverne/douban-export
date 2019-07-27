#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import abc


def r0(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(0)
    return ''


class BaseReview:
    def __init__(self):
        self.title = ''
        self.url = ''
        self.id = ''
        self.content = ''
        self.publish_time = ''
        self.useful_count = 0
        self.useless_count = 0
        self.total_count = 0

    @abc.abstractmethod
    def parse(self, item):
        raise NotImplementedError

    def update(self, raw_content):
        self.content = raw_content['html']
        if 'votes' in raw_content:
            raw_votes = raw_content['votes']
            if 'useful_count' in raw_votes:
                self.useful_count = raw_votes['useful_count']
            if 'useless_count' in raw_votes:
                self.useless_count = raw_votes['useless_count']
            if 'totalcount' in raw_votes:
                self.total_count = raw_votes['totalcount']

    def __str__(self):
        s = []
        for k in self.__dict__:
            s.append("{key}={value}".format(key=k, value=self.__dict__.get(k)))
        return ', '.join(s)

    def __repr__(self):
        return self.__str__()


class BaseExporter:

    def get_review_content(self, id):
        url = 'https://www.douban.com/j/review/{}/full'.format(id)
        r = requests.get(url, headers={
            'Host': 'movie.douban.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        })
        return r.json()