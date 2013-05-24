#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import hashlib
import os


CACHE = 'cache'


def filepath(name):
    return os.path.join(CACHE, name + '.pkl')


def dump(name, o):
    if not os.path.exists(CACHE):
        os.mkdir(CACHE)
    with open(filepath(name), 'wb') as f:
        pickle.dump(o, f)


def cached(fn):
    def inner(*args, **kargs):
        b = pickle.dumps(args) + pickle.dumps(kargs)
        name = hashlib.sha1(b).hexdigest()
        if os.path.exists(filepath(name)):
            with open(filepath(name), 'rb') as f:
                res = pickle.load(f)
        else:
            try:
                res = fn(*args, **kargs)
            except:
                raise
            else:
                dump(name, res)
        return res
    return inner
