import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from google.items import GoogleItem
from scrapy.conf import settings


def parsing_rating(line):
	if len(line)>0:
		return line[0][line[0].find("alt"):]
	else:
		return ""

class GoogleSpider(CrawlSpider):
	name = 'google'
	allowed_domains = ['google.com']
	# rules = (Rule(LxmlLinkExtractor(allow=(r'\/([A-Z])([A-Z0-9]{9})'),deny=('')),callback='parse_item'),Rule(LxmlLinkExtractor(allow=(''))),),)

	# rules = (Rule(LxmlLinkExtractor(allow=(r'https://www.tripadvisor.com/Attraction_Review.*')),callback='parse_trip', process_links='process_links'),)
	rules = (Rule(LxmlLinkExtractor(allow=(r'https://www.google.com/.*')),callback='parse_search'),Rule(LxmlLinkExtractor(allow=(''))),follow=False)

	def __init__(self,*args, **kwargs):
		super(TripadvisorSpider, self).__init__(*args, **kwargs)
		start_url='https://www.tripadvisor.com/Attractions-g187337-Activities-Frankfurt_Hesse.html'
		# start_url='https://www.tripadvisor.com/'
		self.start_urls = [start_url]
	

	def parse_trip(self,response):
		item = GoogleItem()
		print "\n\n---------------------START-----------------------"
		print response.url
		# print response.xpath('//a/@href').extract()
		# try:
		item['name'] = response.xpath('//*[@id="HEADING"]/text()').extract()[0].encode('ascii','ignore')
		# item['rating'] = parsing_rating(response.xpath('//*[@id="HEADING_GROUP"]/div/div[2]/div[1]/div/span/img').extract())
		# item['neighborhood'] = response.xpath('//*[@id="MAP_AND_LISTING"]/div[2]/div/div[2]/div/div[1]/div/address/span/span').extract()
		# item['classification'] = response.xpath('//*[@id="HEADING_GROUP"]/div/div[3]/div[2]/div').extract()
		item['url'] = response.url
		# item['price'] = response.xpath('//*[@id="ABOVE_THE_FOLD"]/div[2]/div[1]/div/div[2]/div/div[1]/div/div[2]/div[1]/text()').extract()
		# item['hours'] = response.xpath('//*[@id="MAP_AND_LISTING"]/div[2]/div/div[2]/div/div[4]/div/div[2]/div').extract()
		# item['desc'] = response.xpath('//*[@id="OVERLAY_CONTENTS"]/div/p/text()').extract()
		# item['desc'] = [desc.encode('ascii','ignore') for desc in response.xpath('//*[@id="feature-bullets"]/ul/li/span/text()').extract() ]
		# usernames = response.xpath('//*[@class="username mo"]').extract()
		# reviews = response.xpath('//*[@class="partial_entry"]/text()').extract()
		# item['reviews'] = zip(usernames,reviews)
		print "\n\n---------------------------------------------------"
		print(item)

		# except:
		# 	print('Not a product!')
		# 	item = None
		yield item

	def process_links(self,links):
		print "\n       LINKS"
		links_list = []
		for i in links:
			if "https://www.tripadvisor.com/Attraction_Review" in i.url:
				links_list.append(i)
				print i.url
		return links_list

	def dummy(self,response):
		print(str(response.url))