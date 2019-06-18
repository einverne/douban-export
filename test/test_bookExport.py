#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase

from exporter.book import BookExport
from utils.logutil import get_logger

log = get_logger(__name__)

class TestBookExport(TestCase):

    def setUp(self):
        self.exporter = BookExport("einverne")

    def test_get_books(self):
        books = self.exporter.get_books(BookExport.READ)
        for book in books:
            log.debug(book)
            self.assertIsNotNone(book, "book object fetch failed")
            self.assertNotEqual(book.title, '', 'book title fetch failed')
            break

    def test_get_read(self):
        readed = self.exporter.get_read()
        for b in readed:
            log.debug(b)
            self.assertIsNotNone(b, 'book object fetch failed')
            self.assertNotEqual(b.title, '', 'book title fetch failed')
            break

    def test_get_wish(self):
        wish = self.exporter.get_wish()
        for b in wish:
            log.debug(b)
            self.assertIsNotNone(b, 'book object fetch failed')
            self.assertNotEqual(b.title, '', 'book title fetch failed')
            break

    def test_get_reading(self):
        reading = self.exporter.get_reading()
        for b in reading:
            log.debug(b)
            self.assertIsNotNone(b, 'book object fetch failed')
            self.assertNotEqual(b.title, '', 'book title fetch failed')
            break

    # def test_get_reviews(self):
        # readed = self.exporter.get_reviews()
        # for b in readed:
        #     log.debug(b)
        #     self.assertIsNotNone(b, 'book object fetch failed')
        #     self.assertNotEqual(b.title, '', 'book title fetch failed')
        #     break


if __name__ == '__main__':
    unittest.main()