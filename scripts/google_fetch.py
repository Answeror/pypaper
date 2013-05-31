#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.getcwd())


from pypaper import log
from pypaper.google import Archive


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('bibtex', help='bibtex file')
    p.add_argument('-c', '--cache', help='cache directory', default='cache')
    p.add_argument('-d', '--database', help='database file', default='google.db')
    p.add_argument('-w', '--wait', help='interval between two query', default=30)
    args = p.parse_args()

    log.init(os.path.join(args.cache, 'google.log'), stdout=True)
    arc = Archive(args.database, interval=float(args.wait))
    arc.import_bibtex(args.bibtex)
