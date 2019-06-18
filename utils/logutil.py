#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
from threading import Lock

cache = {}
lock = Lock()


def get_logger(logger_name):
    # logging.getLogger 获取单例，多次调用会加多个handler，重复写的问题
    global cache
    with lock:
        if not cache.get(logger_name):
            cache[logger_name] = _get_logger(logger_name)
    return cache.get(logger_name)


def _get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    level = "DEBUG"
    logger.setLevel(level)
    logger.propagate = False  # disable dup celery log
    ch = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)6s] [%(pathname)s:%(lineno)s - %(funcName)s] '
                                  '%(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
