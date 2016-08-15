# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import pymongo library
import pymongo
from pymongo import MongoClient

from scrapy.conf import settings

products = {}

class FindagravePipeline(object):
	# For pymongo
	def __init__(self):
		client = MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
			)
		db = client[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		print("\nUpdating the MongoDB ...")
		return item
