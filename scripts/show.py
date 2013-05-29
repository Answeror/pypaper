#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
sys.path.append(os.getcwd())


from pypaper import log
from pypaper.google import Archive
from operator import attrgetter as attr


def write(article, out):
    out.write('%04d %s\n' % (article.citation_count, article.title.encode('utf-8')))


def ordered(articles):
    return sorted(articles, key=attr('citation_count'), reverse=True)


def whole(arc, out):
    for a in ordered(arc.articles):
        write(a, out)


def query(arc, out, bibtex):
    for a in ordered(arc.query(bibtex=bibtex)):
        write(a, out)


def deal(out, bibtex_path):
    log.init('temp/bib.log', stdout=True)
    arc = Archive('temp/all.db')
    if bibtex_path:
        query(arc, out, bibtex_path)
    else:
        whole(arc, out)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('bibtex')
    p.add_argument('-o', '--output', help='output file')
    args = p.parse_args()
    if args.output:
        with open(args.output, 'wb') as f:
            deal(f, args.bibtex)
    else:
        deal(sys.stdout, args.bibtex)
