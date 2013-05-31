#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
sys.path.append(os.getcwd())


from pypaper import log
from pypaper.google import Archive
from operator import attrgetter as attr


def write(article, out):
    out.write('%05d %s\n' % (article.citation_count, article.title.encode('utf-8')))


def ordered(articles):
    return sorted(articles, key=attr('citation_count'), reverse=True)


def whole(arc, out):
    for a in ordered(arc.articles):
        write(a, out)


def query(arc, out, bibtex):
    for a in ordered(arc.query(bibtex=bibtex)):
        write(a, out)


def deal(out, bibtex, cache, database, wait):
    log.init(os.path.join(cache, 'google.log'), stdout=True)
    arc = Archive(database, interval=wait)
    if bibtex:
        query(arc, out, bibtex)
    else:
        whole(arc, out)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('bibtex', help='bibtex file')
    p.add_argument('-c', '--cache', help='cache directory', default='cache')
    p.add_argument('-d', '--database', help='database file', default='google.db')
    p.add_argument('-o', '--output', help='output file', default='out.txt')
    p.add_argument('-w', '--wait', help='interval between two query', default=30)
    args = p.parse_args()

    if not os.path.exists(args.cache):
        os.makedirs(args.cache)

    with open(args.output, 'wb') as f:
        deal(f, args.bibtex, args.cache, args.database, float(args.wait))
