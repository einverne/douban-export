#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(0)
    return ''
