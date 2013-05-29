#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


citation_table = Table(
    'citation',
    Base.metadata,
    Column('parent_id', Integer, ForeignKey('article.id'), primary_key=True),
    Column('child_id', Integer, ForeignKey('article.id'), primary_key=True)
)


class Article(Base):

    __tablename__ = 'article'

    id = Column(String, primary_key=True)
    title = Column(String)
    gn = Column(String)
    year = Column(String, default=None)
    author = Column(String, default=None)
    url = Column(String, default=None)
    citation_count = Column(Integer, default=None)
    version_count = Column(Integer, default=None)
    citation_url = Column(String, default=None)
    version_url = Column(String, default=None)
    related_url = Column(String, default=None)
    references = relationship(
        'Article',
        secondary=citation_table,
        primaryjoin=id == citation_table.c.parent_id,
        secondaryjoin=id == citation_table.c.child_id
    )

    def __init__(
        self,
        id,
        title,
        year=None,
        author=None,
        url=None,
        citation_count=None,
        version_count=None,
        citation_url=None,
        version_url=None,
        related_url=None
    ):
        self.id = id
        self.title = title
        from gn import gn
        self.gn = gn(self.title)
        for name in (
            'year',
            'author',
            'url',
            'citation_count',
            'version_count',
            'citation_url',
            'version_url',
            'related_url'
        ):
            if locals()[name] is not None:
                setattr(self, name, locals()[name])


class Repo(object):

    def __init__(self, path):
        from sqlalchemy import create_engine
        self.engine = create_engine('sqlite:///' + path, echo=False)
        Base.metadata.create_all(self.engine)
        from sqlalchemy.orm import sessionmaker
        self.Session = sessionmaker(bind=self.engine)

    def session(self):
        return Session(self.Session())


class Session(object):

    def __init__(self, impl):
        self.impl = impl

    def add(self, *args):
        for arg in args:
            assert type(arg) in [Article], type(arg)
        self.impl.add_all(args)

    def add_or_update(self, *args):
        for arg in args:
            assert type(arg) in [Article], type(arg)
            arg = self.impl.merge(arg)
            self.impl.add(arg)

    @property
    def articles(self):
        return self.impl.query(Article).all()

    def commit(self):
        self.impl.commit()

    def article_by_id(self, id):
        return self.impl.query(Article).filter(Article.id == id).first()

    def has_id(self, id):
        return self.impl.query(Article).filter(Article.id == id).first() is not None

    def has_title(self, title):
        return self.impl.query(Article).filter(Article.title == title).first() is not None

    def has_prob(self, gn, year=None):
        return self.article_prob(gn=gn, year=year) is not None

    def articles_prob(self, gn, year=None):
        q = self.impl.query(Article).filter(Article.gn == gn)
        if year is not None:
            q = q.filter(Article.year == year)
        return q.all()

    def article_prob(self, gn, year=None):
        q = self.impl.query(Article).filter(Article.gn == gn)
        if year is not None:
            t = q.filter(Article.year == year)
            if t.first() is not None:
                q = t
        return q.first()
