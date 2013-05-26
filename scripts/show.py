#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd())


from pypaper import log
from pypaper.google import Archive


if __name__ == '__main__':
    log.init('temp/bib.log', stdout=True)
    arc = Archive('temp/all.db')
    ps = arc.articles
    from operator import attrgetter as attr
    ps = sorted(ps, key=attr('citation_count'), reverse=True)
    for i, p in zip(range(65536), ps):
        print('%04d %s' % (p.citation_count, p.title.encode('utf-8')))
