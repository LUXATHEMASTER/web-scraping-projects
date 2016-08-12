# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    rating = scrapy.Field()
    neighborhood = scrapy.Field()
    classification = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    hours = scrapy.Field()
    desc = scrapy.Field()
    reviews = scrapy.Field()