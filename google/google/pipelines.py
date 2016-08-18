# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Importing pymongo
import pymongo
from pymongo import MongoClient

from scrapy.conf import settings

products = {}


class GooglePipeline(object):

	# For Mongodb
	def __init__(self):
		client = MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)

		db = client[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		print("\nUpdating the MongoDB ...")
		if item is not None:
			if item['name'] not in products:
				products[item['name']] = item
				currItem = self.collection.find_one({'name':item['name']})

				if currItem is None:
					# if the item not already in the list then just insert
					self.collection.insert(dict(item))
				else:
					# append the new price if it is in the list
					newPrice = currItem['price'] + item['price']
					self.collection.update({'name':currItem['name']},{'$set':{'price':newPrice}})

		return item
