import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from amazonscraping_mongodb.items import AmazonscrapingMongodbItem
import datetime
from scrapy.conf import settings

class AmazonSpider(CrawlSpider):
	name = 'jomashop'
	allowed_domains = ['amazon.in']
	rules = (Rule(LxmlLinkExtractor(allow=(r'https://www.amazon.com/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Ajomashop&page=2&keywords=jomashop&ie=UTF8&qid=1472015227&spIA=.*')),follow=True),
			 Rule(LxmlLinkExtractor(allow=(r'https://www.amazon.com/.*ref=sr_.*?ie=UTF8&qid=1472015292&sr=.*&keywords=jomashop.*')),callback='parse_item',follow=False),)

	def __init__(self, *args, **kwargs):
		super(AmazonSpider, self).__init__(*args, **kwargs)
		start_url = "https://www.amazon.com/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Ajomashop&page=1&keywords=jomashop&ie=UTF8&qid=1472015227&spIA=B00Y1MHRG8,B01AWTSPPA,B01EIA2YXI,B00K5LVHII"
		self.start_urls = [start_url]
	
		
	def parse_item(self,response):
		# print(str(response.url))
		item = AmazonscrapingMongodbItem()
		try:
			name = response.xpath('//*[@id="productTitle"]/text()').extract()[0].encode('ascii','ignore')
			item['name'] = name.strip().split("\n")
			item['reviews'] = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract()[0].encode('ascii','ignore')
			item['url'] = response.url
			# print(response.xpath('//*[@id="avgRating"]/span/text()').extract())
			item['rating'] = response.xpath('//*[@id="avgRating"]/span/text()').extract()[0].encode('ascii','ignore').replace('\n',' ').strip()
			item['pid'] = response.url.split('/ref=')[0].split('/')[-1].encode('ascii','ignore')
			item['price'] = [response.xpath('//*[@id="price"]/table//span[starts-with(@id,"priceblock")]//text()').extract()[1].encode('ascii','ignore').strip()]
			item['desc'] = [desc.encode('ascii','ignore') for desc in response.xpath('//*[@id="feature-bullets"]/ul/li/span/text()').extract() ]
			item['timestamp'] = [str(datetime.datetime.now())]
			print(item)
		except:
			print('Not a product!')
			item = None
		yield item

	def dummy(self,response):
		print(str(response.url))