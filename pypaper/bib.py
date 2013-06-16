#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import yapbib.biblist as biblist

def parse_bibtex(f):
    b = biblist.BibList()
    ret = b.import_bibtex(f)
    if not ret:
        try:
            f.seek(0)
            content = '\n' + f.read()
        except:
            content = f
        logging.debug('parse bibtex failed:%s' % content)
        return None
    return b
