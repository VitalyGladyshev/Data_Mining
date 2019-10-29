# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
# from sqldatabase.database import AvitoRealty
# from sqldatabase.models import Kvart, Photos, Authors, Base
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class HhPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        self.data_base = client.hh_db

        # db_url = r'sqlite:///C:\\Projects\\Data_Mining\\avito_realty.sqlite'
        # self.db = AvitoRealty(Base, db_url)

    def process_item(self, item, spider):
        hh_coll = self.data_base[spider.name]
        hh_coll.insert_one(item)
        # if spider.name == 'avito_realty':
        #     pass
        return item


class AvitoPhotosPipelines(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    pass

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

        # try:
        #     av_kv = Kvart(item['name'], item['url'], item['price'], item['address'])
        # except Exception as e:
        #     print(e)
        # self.db.session.add(av_kv)
        # self.db.session.commit()
        #
        # return item

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