#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import yapbib.biblist as biblist


class ACM(object):

    def __init__(self, id):
        self.id = id

    @property
    def title(self):
        if not hasattr(self, 'b'):
            self.b = self._full_bibtex()
        return self.b.get_items()[0]['title']

    @staticmethod
    def from_url(url):
        from urlparse import urlparse, parse_qs
        words = parse_qs(urlparse(url).query)['id'][0].split('.')
        assert len(words) == 2
        return ACM(id=words[1])

        #import re
        #try:
            #content = urlread(url)
            #return ACM(id=re.search(r"document.cookie = 'picked=' \+ '(\d+)'", content).group(1))
        #except:
            #print(url)
            #return None

    @staticmethod
    def from_title(title):
        from urllib import urlencode
        url = 'http://dl.acm.org/results.cfm'
        d = pq(urlread(url + '?' + urlencode({'query': title})))
        return ACM.from_url(d('a.medium-text').eq(0).attr('href'))

    @staticmethod
    def from_bibtex(f):
        b = biblist.BibList()
        ret = b.import_bibtex(f)
        assert ret
        return [ACM.from_title(it['title']) for it in b.get_items()]

    def export_bibtex(self, f):
        b = self._full_bibtex()
        b.export_bibtex(f)

    def _full_bibtex(self):
        b = self._original_bibtex()
        it = b.get_items()[0]
        it['abstract'] = self._abstract()
        return b

    def _original_bibtex(self):
        TEMPLATE = 'http://dl.acm.org/exportformats.cfm?id=%s&expformat=bibtex&_cf_containerId=theformats_body&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=142656B43EEEE8D6E34FC208DBFCC647&_cf_rc=3'
        url = TEMPLATE % self.id
        d = pq(urlread(url))
        content = d('pre').text()
        from StringIO import StringIO
        f = StringIO(content)
        b = biblist.BibList()
        ret = b.import_bibtex(f)
        assert ret, content
        return b

    def _abstract(self):
        TEMPLATE = 'http://dl.acm.org/tab_abstract.cfm?id=%s&usebody=tabbody&cfid=216938597&cftoken=33552307&_cf_containerId=abstract&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=142656B43EEEE8D6E34FC208DBFCC647&_cf_rc=0'
        url = TEMPLATE % self.id
        d = pq(urlread(url))
        return d.text()

    def download_pdf(self):
        TEMPLATE = 'http://dl.acm.org/ft_gateway.cfm?id=%s&ftid=723552&dwn=1&CFID=216938597&CFTOKEN=33552307'
        url = TEMPLATE % self.id
        content = urlread(url)
        filename = escape(self.title) + '.pdf'
        import os
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(content)


def escape(name):
    #import string
    #valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    #return ''.join([ch if ch in valid_chars else ' ' for ch in name])
    from gn import Gn
    gn = Gn()
    return gn(name)


def urlread(url):
    import urllib2
    import cookielib
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    page = urllib2.urlopen(req)
    return page.read()


def from_clipboard():
    import win32clipboard
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def test_download():
    bib = ACM.from_url('http://dl.acm.org/citation.cfm?id=1672308.1672326&coll=DL&dl=ACM&CFID=216938597&CFTOKEN=33552307')
    bib.download_pdf()


def test_from_url():
    bib = ACM.from_url('http://dl.acm.org/citation.cfm?id=1672308.1672326&coll=DL&dl=ACM&CFID=216938597&CFTOKEN=33552307')
    print(bib.id)


def test_from_title():
    bib = ACM.from_title('Applications of mobile activity recognition')
    print(bib.id)


def get_params():
    import sys
    return sys.argv[1] if len(sys.argv) > 1 else from_clipboard()


def download_bibtex(arg):
    bib = ACM.from_url(arg)
    #from StringIO import StringIO
    #f = StringIO()
    bib.export_bibtex('out.bib')
    #print(f.getvalue())


def download_pdf(arg):
    import time
    bibs = ACM.from_bibtex(arg)
    print('bibs loaded')
    for bib in bibs:
        for i in range(10):
            try:
                print(bib.title)
                bib.download_pdf()
                time.sleep(10)
            except:
                print('failed')
            else:
                print('done')
                break


if __name__ == '__main__':
    arg = get_params()
    if arg.endswith('.bib'):
        download_pdf(arg)
    else:
        download_bibtex(arg)
