import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from amazonscraping_mongodb.items import AmazonscrapingMongodbItem
import datetime
from scrapy.conf import settings
from scrapy.shell import inspect_response

class AmazonSpider(CrawlSpider):
	# handle_httpstatus_list = [301, 302, 303]
	name = 'jomashop'
	allowed_domains = ['amazon.com']
	# rules = (Rule(LxmlLinkExtractor(allow=(r'.*jomashop.*')),follow=True,),
	# 		 Rule(LxmlLinkExtractor(allow=(r'.*&keywords=jomashop.*')),callback='parse_item',follow=False,),
	# 		 Rule(LxmlLinkExtractor(allow=('')),follow=False,))
	rules = (Rule(LxmlLinkExtractor(allow=(r'/*amazon\.com.*page\=.*Jomashop'),deny=(r'product\-reviews',r'offer\-listing',r'ebook')),follow=True),
		 	 Rule(LxmlLinkExtractor(allow=(r'.*\/dp\/.*'),deny=(r'product\-reviews',r'offer\-listing',r'ebook')),callback='parse_item',follow=False),)
			 # Rule(LxmlLinkExtractor(allow=('')),follow=False),)

	def __init__(self, 
			start_url="https://www.amazon.com/s/ref=w_bl_sl_s_wa_web_7141123011?ie=UTF8&node=7141123011&field-keywords=Jomashop",
			*args, **kwargs):
		super(AmazonSpider, self).__init__(*args, **kwargs)
		self.start_urls = [start_url]

	def parse_item(self,response):
		# print(str(response.url))
		item = AmazonscrapingMongodbItem()
		print('\n--------------------------------------------------\n')
		print(response.url)

		referer_url = response.request.headers.get('Referer', None)
		print("REFERER IS")
		print(referer_url)
		if "omashop" in referer_url:
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
		else:
			item = None

		yield item

	def dummy(self,response):
		print(str(response.url))