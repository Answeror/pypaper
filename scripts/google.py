#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd())


from pypaper import log
from pypaper.google import Paper


def from_clipboard():
    import win32clipboard
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def get_params():
    return sys.argv[1] if len(sys.argv) > 1 else from_clipboard()


if __name__ == '__main__':
    log.init('temp/bib.log', stdout=True)
    arg = get_params()
    ps = Paper.from_bibtex_file(arg)
    from operator import attrgetter as attr
    ps = sorted(ps, key=attr('citation_count'), reverse=True)
    for i, p in zip(range(65536), ps):
        print('%d\t%s' % (p.citation_count, p.title[:74]))
