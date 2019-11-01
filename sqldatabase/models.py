from sqlalchemy import (Table,
                        Column,
                        ForeignKey,
                        String,
                        Integer,
                        DECIMAL)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# associative_tag_post = Table('associative_tag_post',
#                              Base.metadata,
#                              Column('blog_post', Integer, ForeignKey('blogpost.id')),
#                              Column('blog_tags', Integer, ForeignKey('tags.id')))


class Kvart(Base):
    __tablename__ = 'kvart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    url = Column(String, unique=True)
    price = Column(String)  # DECIMAL)
    address = Column(String)
    # author = Column(Integer, ForeignKey('authors.id'))
    # authors = relationship('Authors', backref='posts')
    # photo = relationship('Photos', secondary=associative_tag_post, backref='posts')

    def __init__(self, name, url, price, address):
        self.name = name
        self.url = url
        self.price = price
        self.address = address
        # if photo:
        #     self.photo.extend(photo)
        # if author:
        #     self.author = author


class Photos(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)

    def __init__(self, url):  # **kwargs
        self.url = url


class Authors(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    name = Column(String)

    def __init__(self, url, name):
        self.url = url
        self.name = name
