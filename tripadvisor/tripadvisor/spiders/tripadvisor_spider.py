import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from tripadvisor.items import TripadvisorItem
from scrapy.conf import settings

class TripadvisorSpider(CrawlSpider):
	name = 'tripadvisor'
	allowed_domains = ['tripadvisor.in']
	# rules = (Rule(LxmlLinkExtractor(allow=(r'\/([A-Z])([A-Z0-9]{9})'),deny=('')),callback='parse_item'),Rule(LxmlLinkExtractor(allow=(''))),)
	rules = (Rule(LxmlLinkExtractor(allow=('')),callback='parse'),Rule(LxmlLinkExtractor(allow=(''))),)

	def __init__(self,*args, **kwargs):
		super(TripadvisorSpider, self).__init__(*args, **kwargs)
		start_url='https://www.tripadvisor.com/Attractions-g187337-Activities-Frankfurt_Hesse.html'
		self.start_urls = [start_url]
	
		
	def parse(self,response):
		# print(str(response.url))
		item = TripadvisorItem()
		print "\n\n---------------------START-----------------------"
		print response.url
		# try:
		item['name'] = response.xpath('//*[@id="HEADING"]/text()').extract()[0].encode('ascii','ignore')
		item['rating'] = response.xpath('//*[@id="HEADING_GROUP"]/div/div[2]/div[1]/div/span/img').extract()
		item['neighborhood'] = response.xpath('//*[@id="MAP_AND_LISTING"]/div[2]/div/div[2]/div/div[1]/div/address/span/span').extract()
		item['classification'] = response.xpath('//*[@id="HEADING_GROUP"]/div/div[3]/div[2]/div').extract()
		item['url'] = response.url
		item['price'] = response.xpath('//*[@id="ABOVE_THE_FOLD"]/div[2]/div[1]/div/div[2]/div/div[1]/div/div[2]/div[1]/text()').extract()
		item['hours'] = response.xpath('//*[@id="MAP_AND_LISTING"]/div[2]/div/div[2]/div/div[4]/div/div[2]/div').extract()
		item['desc'] = response.xpath('//*[@id="MAP_AND_LISTING"]/div[2]/div/div[2]/div/div[6]/div/p').extract()
		# item['desc'] = [desc.encode('ascii','ignore') for desc in response.xpath('//*[@id="feature-bullets"]/ul/li/span/text()').extract() ]
		item['reviews'] = response.xpath('//*[@class="reviewSelector"]').extract()
		print "\n\n---------------------------------------------------"
		print(item)
		# except:
		# 	print('Not a product!')
		# 	item = None
		yield item

	def dummy(self,response):
		print(str(response.url))