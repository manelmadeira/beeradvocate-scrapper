# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import log
from scrapy.conf import settings
from beerscrapper.items import *


class BeerscrapperPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

        # clear collection
        self.collection.delete_many({})


    def process_item(self, item, spider):
        if not isinstance(item, BeerItem):
            return item

        self.collection.insert(dict(item))
        log.msg(
            "Beer ({name}) added to MongoDB database!".format(
                name=str(item["name"])
            ),
            level=log.DEBUG,
            spider=spider
        )

        return item
