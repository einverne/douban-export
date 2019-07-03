#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


def get_args():
    parser = argparse.ArgumentParser(prog="Douban exporter",
                                     description="""
                                     A tiny tool used to export douban data
                                     """)
    parser.add_argument("u", metavar='UserId', help="username or userId")
    parser.add_argument("movie", help="dump movie info")
    parser.add_argument("book", help="dump book info")
    parser.add_argument("music", help="dump music info")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    return parser.parse_args()
