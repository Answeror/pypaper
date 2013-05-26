#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
from config import Config


def rep(s, subs=[]):
    if not s:
        return s
    head, tail = os.path.splitext(s)
    subed = head
    for pattern, replace in subs:
        subed = re.sub(pattern, replace, subed)
    if not subed:
        return subed
    trimed = re.search(r'\W*(.*\w)\W*', subed).group(1)
    return re.sub(r'\W+', '-', trimed.lower()) + tail.lower()


def reppath(path, subs=[]):
    parts = os.path.split(path)
    return os.path.join(*(list(parts[:-1]) + [rep(parts[-1], subs)]))


class Gn(object):

    def __init__(self):
        self.conf = Config()

    def __call__(self, name):
        return reppath(name, self.conf.subs)


gn = Gn()
