#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def decode(bs, encodings=['utf-8', 'cp936', 'gbk', 'gb18030', 'big5', 'latin1']):
    for en in encodings:
        try:
            return bs.decode(en)
        except:
            pass
    raise RuntimeError('Decoding failed.')


class Config(object):

    def __init__(self, f=os.path.expanduser(os.path.join('~', '.gn'))):
        if type(f) is str:
            if not os.path.exists(f):
                open(f, 'w').close()
                s = ''
            else:
                with open(f, 'rb') as f:
                    s = decode(f.read())
        else:
            s = f.read()
        lines = s.split('\n')
        self.subs = []
        if lines and len(lines[0]) == 1:
            sep = lines[0]
            for line in lines[1:]:
                tokens = line.split(sep)
                if len(tokens) == 2 and tokens[0]:
                    self.subs.append((tokens[0], tokens[1]))
