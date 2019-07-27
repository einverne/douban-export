#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from exporter import r1


class NoteInfo:
    def __init__(self):
        self.title = ''
        self.url = ''
        self.id = ''
        self.content = ''
        self.publish_time = ''

    @classmethod
    def parse(cls, item):
        instance = cls()
        instance.title = item.select('h3')[0].text.strip()
        instance.url = item['data-url']
        instance.id = r1(r'\d+', instance.url)
        instance.publish_time = item.select('.pub-date')[0].text.strip()
        return instance

    def __str__(self):
        s = []
        for k in self.__dict__:
            s.append("{key}={value}".format(key=k, value=self.__dict__.get(k)))
        return ', '.join(s)

    def __repr__(self):
        return self.__str__()


class NotesExport:
    """
    遍历网页的问题可能被豆瓣反爬虫机制伤及，如果能够直接从接口 dump 数据就比较快
    """
    BASE_URL = 'https://www.douban.com/people/{}'

    def __init__(self, nickname):
        self.user_url = NotesExport.BASE_URL.format(nickname)

    def get_notes(self):
        """
        Get one's all notes

        https://music.douban.com/people/einverne/reviews?start=0
        https://music.douban.com/j/review/10000057/fullinfo?show_works=False
        """
        start = 0
        while True:
            note_list = self.__get_notes_list(start)
            step = len(note_list)
            if step == 0:
                break
            for note in note_list:
                note_info = NoteInfo.parse(note)
                content = self.get_note_content(note_info.id)
                bs = BeautifulSoup(content, 'html.parser')
                note_info.content = bs.text
                yield note_info
            if step < 10:
                break
            start += step

    def __get_notes_list(self, start=0):
        url = self.user_url + '/notes'
        r = requests.get(url, params={
            'type': 'note',
            'start': start
        }, headers={
            'Host': 'www.douban.com',
            'Referer': self.user_url + '/notes?start=0&type=note',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.select('.note-container')

    def get_note_content(self, id='721551646'):
        """
        Get all note content by pass ID, return the content str
            https://www.douban.com/j/note/{id}/full
        :param id:
        :return:
        """
        url = "https://www.douban.com/j/note/{}/full".format(id)
        r = requests.get(url, headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip',
            'Host': 'www.douban.com',
            'Referer': self.user_url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        })
        return r.json()['html']


if __name__ == '__main__':
    m = NotesExport('einverne')
    for note in m.get_notes():
        print(note)
