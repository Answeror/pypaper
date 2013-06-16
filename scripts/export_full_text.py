#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from pypaper import log
from pypaper.mendeley import Mendeley


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('bibtex', help='bibtex file')
    p.add_argument('-d', '--database', help='database bibtex file')
    p.add_argument('-o', '--output', help='output directory', default='out')
    args = p.parse_args()

    log.init('pypaper.log', stdout=False)
    mendeley = Mendeley(bibtex_path=args.database)
    mendeley.export_full_text(args.bibtex, args.output)
