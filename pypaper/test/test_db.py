#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .. import db
import tempfile
import shutil
import os
from nose.tools import assert_true, assert_equal


class Test(object):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.repo = db.Repo(os.path.join(self.root, 'bib.db'))

    def tearDown(self):
        try:
            shutil.rmtree(self.root)
        except:
            pass

    def test_add(self):
        parent = db.Article(
            id='a',
            title='a',
            citation_count=0
        )
        children = [
            db.Article(
                id='b',
                title='b',
                citation_count=1
            ),
            db.Article(
                id='c',
                title='c',
                citation_count=1
            )
        ]
        parent.references.extend(children)
        con = self.repo.session()
        con.add([parent] + children)
        con.commit()
        con = self.repo.session()
        assert_equal(len(con.articles), 3)
        assert_true(not con.article_by_id('a') is None)
        assert_equal(len(con.article_by_id('a').references), 2)
