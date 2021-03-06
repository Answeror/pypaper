#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging


def init(path=os.path.expanduser('~/.bib.log'), stdout=False):
    LEVEL = logging.DEBUG
    logging.basicConfig(
        filename=path,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=LEVEL
    )
    import sys
    if stdout:
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.INFO),
        logging.getLogger().addHandler(h)
