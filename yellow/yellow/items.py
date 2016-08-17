# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YellowItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	Company = scrapy.Field()
	Contact = scrapy.Field()
	PhoneNumber = scrapy.Field()
	CellPhoneNumber = scrapy.Field()
	PhysicalAddress = scrapy.Field()
	MailingAddress = scrapy.Field()
	email = scrapy.Field()
	url = scrapy.Field()