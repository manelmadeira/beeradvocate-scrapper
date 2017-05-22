# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    ba_score = scrapy.Field()
    ba_ratings = scrapy.Field()
    picture = scrapy.Field()
    producer = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    website = scrapy.Field()
    style = scrapy.Field()
    style_id = scrapy.Field()
    alcohol = scrapy.Field()
