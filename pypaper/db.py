#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Date, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


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
    citation_count = Column(Integer)
    references = relationship(
        'Article',
        secondary=citation_table,
        primaryjoin=id == citation_table.c.parent_id,
        secondaryjoin=id == citation_table.c.child_id
    )

    def __init__(self, id, title, citation_count):
        self.id = id
        self.title = title
        self.citation_count = citation_count


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

    @property
    def articles(self):
        return self.impl.query(Article).all()

    def commit(self):
        self.impl.commit()

    def article_by_id(self, id):
        return self.impl.query(Article).filter(Article.id == id).first()
