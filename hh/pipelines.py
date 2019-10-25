# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# from pymongo import MongoClient
from sqldatabase.database import AvitoRealty
from sqldatabase.models import Kvart, Photos, Authors, Base


class HhPipeline(object):
    def __init__(self):
        # mongo_url = 'mongodb://localhost:27017'
        # client = MongoClient(mongo_url)
        # data_base = client.hh_db
        # self.hh_coll = data_base.hh_coll
        db_url = r'sqlite:///C:\\Projects\\Data_Mining\\avito_realty.sqlite'
        self.db = AvitoRealty(Base, db_url)

    def process_item(self, item, spider):
        try:
            av_kv = Kvart(item['name'], item['url'], item['price'], item['address'])
        except Exception as e:
            print(e)
        self.db.session.add(av_kv)
        self.db.session.commit()

        return item

        # author = self.db.session.query(Authors).filter_by(url=item.get('author_url')).first()
        # if not author:
        #     author = Authors(item.get('author_url'), item.get('author_name'))
        #     self.db.session.add(author)
        #     try:
        #         self.db.session.commit()
        #     except Exception as e:
        #         print(e)
        #
        # tags = [Tags(itm["name"], itm["url"]) for itm in item.get('tags')]