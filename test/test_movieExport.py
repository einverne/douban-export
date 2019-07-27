#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from exporter import *
from exporter.movie import MovieExport
from utils.logutil import get_logger

log = get_logger(__name__)


class TestMovieExport(TestCase):

    def setUp(self):
        self.exporter = MovieExport("einverne")

    def test_get_movies(self):
        movies = self.exporter.get_movies(COLLECT)
        for m in movies:
            log.debug(m)
            self.assertIsNotNone(m, 'content should not be none')
            self.assertNotEqual(m.title, '', 'movie title fetch failed')
            break

    def test_get_watched(self):
        movies = self.exporter.get_watched()
        for m in movies:
            log.debug(m)
            self.assertIsNotNone(m, 'content should not be none')
            self.assertNotEqual(m.title, '', 'movie title fetch failed')
            break

    def test_get_wish(self):
        movies = self.exporter.get_wish()
        for m in movies:
            log.debug(m)
            self.assertIsNotNone(m, 'content should not be none')
            self.assertNotEqual(m.title, '', 'movie title fetch failed')
            break

    def test_get_doing(self):
        movies = self.exporter.get_doing()
        for m in movies:
            log.debug(m)
            self.assertIsNotNone(m, 'content should not be none')
            self.assertNotEqual(m.title, '', 'movie title fetch failed')
            break

    def test_get_reviews(self):
        movies = self.exporter.get_reviews()
        for m in movies:
            log.debug(m)
            self.assertIsNotNone(m, 'content should not be none')
            self.assertNotEqual(m.title, '', 'movie title fetch failed')
            break

    # def test_get_doulist(self):
    #     movies = self.exporter.get_doulist()
    #     for m in movies:
    #         log.debug(m)
    #         self.assertIsNotNone(m, 'content should not be none')
    #         self.assertNotEqual(m.title, '', 'movie title fetch failed')
    #         break

    def test_get_review_content(self):
        c = self.exporter.get_review_content('10124597')
        log.debug(c)
        self.assertIsNotNone(c)


if __name__ == '__main__':
    unittest.main()
