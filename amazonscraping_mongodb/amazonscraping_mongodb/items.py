"""
Scraping Amazon with MongoDB
The script is from
	https://github.com/kbyagnik/Amazon-PriceTracker/blob/master/src/aragog/aragog/items.py
"""

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscrapingMongodbItem(scrapy.Item):
    # define the fields for your item here like:
    pid = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    timestamp = scrapy.Field()
    desc = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
