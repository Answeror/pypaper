#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import yapbib.biblist as biblist
from scholar import ScholarQuerier
from . import db


q = ScholarQuerier()


COMMON_FIELDS = (
    'id',
    'title',
    'year',
    'author',
    'url',
    'citation_count',
    'version_count',
    'citation_url',
    'version_url',
    'related_url'
)


class Article(object):

    @staticmethod
    def from_db(d):
        if d is None:
            return None
        a = Article()
        for name in COMMON_FIELDS:
            assert hasattr(d, name), name
            setattr(a, name, getattr(d, name))
        return a

    @property
    def complete(self):
        """Whether article has complete information."""
        for key in COMMON_FIELDS:
            if not hasattr(self, key) or getattr(self, key) is None:
                return False
        return True

    def to_db(self, a):
        return db.Article(**{name: getattr(a, name) for name in COMMON_FIELDS})

    @property
    def valid(self):
        return hasattr(self, 'id') and self.id and hasattr(self, 'title') and self.title

    @property
    def gn(self):
        from gn import gn
        assert hasattr(self, 'title') and self.title
        return gn(_em(self.title))

    @staticmethod
    def from_dict(d):
        a = Article()
        return a.import_dict(d)

    def import_dict(self, d):
        for key, value in d.items():
            setattr(self, key, value)
        return self

    def google_update(self):
        logging.info('dealing "%s"' % self.title)
        try:
            q.reset()
            q.query(self.title)
            if not q.articles:
                return None
            art = self._select_best(q.articles)
            for key, value in (
                ('id', art['id']),
                ('title', art['title']),
                ('citation_count', art['num_citations']),
                ('url', art['url']),
                ('author', art['author']),
                ('version_count', art['num_versions']),
                ('citation_url', art['url_citations']),
                ('version_url', art['url_versions']),
                ('related_url', art['url_ralted']),
                ('year', art['year'])
            ):
                self._try_update(key, value)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            logging.info('crawl "%s" failed' % self.title)
            logging.exception(e)
            return False
        else:
            logging.info('crawl "%s" done' % self.title)
            return True

    def _try_update(self, key, value):
        if not hasattr(self, key) or value is not None:
            setattr(self, key, value)

    def _select_best(self, articles):
        from gn import gn
        from lcs import lcs
        return min(articles, key=lambda art: lcs(self.gn, gn(_em(art['title']))))


def _em(s):
    return '' if s is None else s


class Archive(object):

    def __init__(self, path, interval=30):
        self.repo = db.Repo(path)
        self.interval = interval

    @property
    def articles(self):
        con = self.repo.session()
        return [Article.from_db(a) for a in con.articles]

    def _parse_bibtex(self, f):
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

    def import_bibtex(self, f, complete=True):
        def need_update(a):
            if self.has_prob(gn=a.gn, year=a.year):
                logging.info('"%s" already in database' % a.title)
                articles = self.articles_prob(gn=a.gn, year=a.year)
                assert articles
                if len(articles) > 1:
                    logging.info('gn "%s" not unique' % a.title)
                    return False
                if complete and not articles[0].complete:
                    logging.info('info not complete, update')
                    return True
                return False
            return True

        b = self._parse_bibtex(f)
        if not b:
            return

        for it in b.get_items():
            try:
                a = Article.from_dict(it)
                if need_update(a):
                    a = self.article_prob(gn=a.gn, year=a.year)
                    if not a:
                        a = Article.from_dict(it)
                    else:
                        a.import_dict(it)
                    if a.google_update():
                        if not a.valid:
                            logging.info('invalid article: "%s"' % a.title)
                        else:
                            self._add_or_update_article(a)
                    self._pause()
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                logging.debug('failed on "%s"' % _em(it['title']))
                logging.exception(e)

    def has(self, id):
        con = self.repo.session()
        return con.has_id(id)

    def has_title(self, title):
        con = self.repo.session()
        return con.has_title(title)

    def has_prob(self, gn, year=None):
        con = self.repo.session()
        return con.has_prob(gn, year)

    def articles_prob(self, gn, year=None):
        con = self.repo.session()
        return [Article.from_db(a) for a in con.articles_prob(gn, year)]

    def article_prob(self, gn, year=None):
        con = self.repo.session()
        return Article.from_db(con.article_prob(gn, year))

    def _add_article(self, a):
        con = self.repo.session()
        con.add(a.to_db(a))
        con.commit()

    def _add_or_update_article(self, a):
        con = self.repo.session()
        con.add_or_update(a.to_db(a))
        con.commit()

    def _pause(self):
        import time
        import random
        time.sleep(self.interval + (random.random() - 0.5) * self.interval / 2.0)

    def query(self, **kargs):
        if 'bibtex' in kargs:
            return self._query_bi_bibtex(kargs['bibtex'])
        else:
            assert False, 'known arguments: %s' % str(kargs.keys())

    def _query_bi_bibtex(self, bibtex):
        b = self._parse_bibtex(bibtex)
        if b is None:
            return []

        articles = []
        for it in b.get_items():
            try:
                a = Article.from_dict(it)
                a = self.article_prob(gn=a.gn, year=a.year)
                if not a is None:
                    articles.append(a)
                else:
                    logging.info('cannot find "%s"' % _em(it['title']))
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                logging.debug('failed on "%s"' % _em(it['title']))
                logging.exception(e)

        return articles
