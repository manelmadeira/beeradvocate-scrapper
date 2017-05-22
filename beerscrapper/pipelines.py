# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from beerscrapper.items import *

class BeerscrapperPipeline(object):
    def process_item(self, item, spider):
        if not isinstance(item, BeerItem):
            return item

        # TODO: handle beer

        return item
