#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import logging
from bib import parse_bibtex


def _copy(src, dst):
    logging.info('copy from %s to %s' % (src, dst))
    shutil.copy(src, dst)


def _escape(path):
    return path.replace(r'$\backslash$', '').replace(':pdf', '')[1:]


class Mendeley(object):

    def __init__(self, bibtex_path):
        self.bibtex_path = bibtex_path

    @property
    def bib(self):
        if not hasattr(self, '_bib'):
            self._bib = parse_bibtex(self.bibtex_path)
        if self._bib is None:
            raise Exception('mendeley bibtex parse failed: %s' % self.bibtex_path)
        return self._bib

    def export_full_text(self, bibtex_path, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        b = parse_bibtex(bibtex_path)
        if b is None:
            return
        for it in b.get_items():
            key = it.key
            item = self.bib.get_item(key)
            if not item:
                logging.info('no such key: %s' % key)
            else:
                if 'file' not in item:
                    logging.info('no file field in %s' % key)
                else:
                    file_path = _escape(item['file'])
                    if not os.path.exists(file_path):
                        logging.info('file not exist: %s' % file_path)
                    else:
                        filename = os.path.basename(file_path)
                        _copy(file_path, os.path.join(output_path, filename))
