#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import yapbib.biblist as biblist


class IEEE(object):

    def __init__(self, id, it=None):
        self.id = id
        if not it is None:
            self.it = it

    @property
    def title(self):
        if not hasattr(self, 'it'):
            self.it = self._full_bibtex().get_items()[0]
        return self.it['title']

    @staticmethod
    def from_url(url):
        return IEEE(id=id_from_url(url))

    @staticmethod
    def from_bibtex_item(it):
        #try:
            #return IEEE(id=id_from_item(it), it=it)
        #except:
            #print(it['title'])
            #raise
        return IEEE(id=id_from_item(it), it=it)

    @staticmethod
    def from_bibtex(f):
        b = biblist.BibList()
        ret = b.import_bibtex(f)
        assert ret
        return [IEEE.from_bibtex_item(it) for it in b.get_items()]

    def export_bibtex(self, f):
        b = self._full_bibtex()
        b.export_bibtex(f)

    def download_pdf(self):
        TEMPLATE = 'http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=%s'
        url = TEMPLATE % self.id
        content = urlread(url)
        url = pq(content)('frame').eq(1).attr('src')
        content = urlread(url)
        filename = escape(self.title) + '.pdf'
        import os
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(content)


def escape(name):
    from gn import Gn
    gn = Gn()
    return gn(name)


import urllib2
import cookielib
cookies = cookielib.LWPCookieJar()
handlers = [
    urllib2.HTTPHandler(),
    urllib2.HTTPSHandler(),
    urllib2.HTTPCookieProcessor(cookies)
    ]
opener = urllib2.build_opener(*handlers)


def urlread(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    page = opener.open(req)
    return page.read()


def from_clipboard():
    import win32clipboard
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def get_params():
    import sys
    return sys.argv[1] if len(sys.argv) > 1 else from_clipboard()


def download_bibtex(arg):
    bib = IEEE.from_url(arg)
    bib.export_bibtex('out.bib')


def download_pdf(arg):
    import time
    import random
    bibs = IEEE.from_bibtex(arg)
    print('bibs loaded')
    for bib in bibs:
        for i in range(1):
            try:
                print(bib.title)
                bib.download_pdf()
                jump = 60 + random.randint(0, 30)
                print('sleep %d' % jump)
                time.sleep(jump)
            except:
                print('failed')
            else:
                print('done')
                break


def id_from_item(it):
    urls = it['url'].split()
    assert urls
    for url in urls:
        try:
            return id_from_url(url)
        except:
            pass
    assert False


def id_from_url(url):
    from urlparse import urlparse, parse_qs
    word = parse_qs(urlparse(url).query)['arnumber'][0]
    assert word
    return word


if __name__ == '__main__':
    arg = get_params()
    if arg.endswith('.bib'):
        download_pdf(arg)
    else:
        download_bibtex(arg)
