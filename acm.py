#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq


class ACM(object):

    def __init__(self, id):
        self.id = id

    @staticmethod
    def from_url(url):
        from urlparse import urlparse, parse_qs
        words = parse_qs(urlparse(url).query)['id'][0].split('.')
        assert len(words) == 2
        return ACM(id=words[1])

    def export_bibtex(self, f):
        b = self._original_bibtex()
        it = b.get_items()[0]
        it['abstract'] = self._abstract()
        b.export_bibtex(f)

    def _original_bibtex(self):
        TEMPLATE = 'http://dl.acm.org/exportformats.cfm?id=%s&expformat=bibtex&_cf_containerId=theformats_body&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=142656B43EEEE8D6E34FC208DBFCC647&_cf_rc=3'
        url = TEMPLATE % self.id
        d = pq(urlread(url))
        content = d('pre').text()
        from StringIO import StringIO
        f = StringIO(content)
        import yapbib.biblist as biblist
        b = biblist.BibList()
        ret = b.import_bibtex(f)
        assert ret
        return b

    def _abstract(self):
        TEMPLATE = 'http://dl.acm.org/tab_abstract.cfm?id=%s&usebody=tabbody&cfid=216938597&cftoken=33552307&_cf_containerId=abstract&_cf_nodebug=true&_cf_nocache=true&_cf_clientid=142656B43EEEE8D6E34FC208DBFCC647&_cf_rc=0'
        url = TEMPLATE % self.id
        d = pq(urlread(url))
        return d.text()


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


if __name__ == '__main__':
    import sys
    bib = ACM.from_url(sys.argv[1] if len(sys.argv) > 1 else from_clipboard())
    #from StringIO import StringIO
    #f = StringIO()
    bib.export_bibtex('out.bib')
    #print(f.getvalue())
