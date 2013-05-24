#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import yapbib.biblist as biblist
from cache import cached
from urllib2 import HTTPError


class Paper(object):

    @staticmethod
    @cached
    def from_title(title):
        try:
            from scholar import ScholarQuerier
            q = ScholarQuerier()
            q.query(title)
            if not q.articles:
                return None
            art = q.articles[0]
            p = Paper()
            p.title = art['title']
            p.citation_count = art['num_citations']
            p.url = art['url']
            p.version_count = art['num_versions']
            p.citation_url = art['url_citations']
            p.version_url = art['url_versions']
            p.year = art['year']
            return p
        except HTTPError as e:
            logging.debug('http %d, title: %s' % (e.code, title))
            raise
        except Exception as e:
            logging.debug('title: %s' % title)
            logging.exception(e)
            raise

    @staticmethod
    def from_bibtex_file(f):
        b = biblist.BibList()
        ret = b.import_bibtex(f)
        if not ret:
            try:
                f.seek(0)
                content = '\n' + f.read()
            except:
                content = f
            logging.debug('parse bibtex failed:%s' % content)
            return []
        res = []
        for it in b.get_items():
            try:
                p = Paper.from_title(it['title'])
            except HTTPError:
                pass
            else:
                res.append(p)
            pause()
        return res


def pause(interval=10):
    import time
    import random
    time.sleep(interval + (random.random() - 0.5) * interval / 2.0)


def from_clipboard():
    import win32clipboard
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def get_params():
    import sys
    return sys.argv[1] if len(sys.argv) > 1 else from_clipboard()


if __name__ == '__main__':
    import log
    log.init('bib.log', stdout=True)
    arg = get_params()
    ps = Paper.from_bibtex_file(arg)
    from operator import attrgetter as attr
    ps = sorted(ps, key=attr('citation_count'), reverse=True)
    for i, p in zip(range(65536), ps):
        print('%d\t%s' % (p.citation_count, p.title[:74]))
