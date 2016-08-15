"""
Web Scraper of findagrave
Location: San Antonio, Texas
"""

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from findagrave.items import FindagraveItem
from scrapy.conf import settings
import re 

def parsing_tag(line):
	start = 0
	newline = ""
	for i in range(len(line)):
		if line[i] == ">":
			start = i+1
		elif line[i] == "<":
			newline += line[start:i]
	return newline

# function to extract out html tags from contents
def parsing_html(line):
	start = 0
	newline = ""
	for i in range(len(line)):
		if line[i:i+3] == "<td":
			newline += "\n"
		if line[i:i+4] == "Plot":
			newline += "\n"
		if line[i] == ">":
			start = i + 1
		elif line[i] == "<":
			if start + 1 < i:
				newline += line[start:i] + " "
	newline = newline.encode('ascii','ignore')
	precontents = newline.split("\n")
	contents = [i for i in precontents if i != '']
	birthdate = contents[1]
	deathdate = contents[3]
	description = contents[4]
	burial = contents[5]
	plot = contents[6]

	return birthdate, deathdate, description, burial, plot

# Clean out name
def parsing_name(line):
	line = line[0]
	return line[line.find("<b>")+3:line.find("</b>")]

class FindagraveSpider(CrawlSpider):
	name = 'findagravesan'
	allowed_domains = ['findagrave.com']
	# rules = (Rule(LxmlLinkExtractor(allow=(r'\/([A-Z])([A-Z0-9]{9})'),deny=('')),callback='parse_item'),Rule(LxmlLinkExtractor(allow=(''))),),)

	# rules = (Rule(LxmlLinkExtractor(allow=(r'https://www.tripadvisor.com/Attraction_Review.*')),callback='parse_trip', process_links='process_links'),)
	rules = (Rule(LxmlLinkExtractor(allow=(r'.*FScityid=1118.*'), deny=(r'.*CRid=.*', r'.*MRid=.*',r'.*=gr.*', r'.*=gs.*', r'.*=cs.*', r'.*=mp.*', r'.*=ss.*', r'.*=mr.*', r'.*=cem.*', r'.*GSvpid.*')), follow=True,),
			 Rule(LxmlLinkExtractor(allow=(r'.*GRid=.*')),callback='parse_grave', follow=False,),
			 Rule(LxmlLinkExtractor(allow=('')), follow=False,))

	def __init__(self,*args, **kwargs):
		super(FindagraveSpider, self).__init__(*args, **kwargs)
		start_url='http://www.findagrave.com/php/famous.php?page=city&FScityid=1118'
		self.start_urls = [start_url]
	

	def parse_grave(self,response):
		item = FindagraveItem()
		print "\n\n---------------------START-----------------------"
		print response.url
		item['name'] = response.xpath('//*[@class="plus2"]').extract()

		if len(item['name']) > 0 and item['name'][0] != '<font size="+2" class="plus2">Become A Member</font>':
			item['name'] = parsing_name(item['name'])
			item['url'] = response.url
			contents = response.xpath('//*[@class="gr"]').extract()

			wrong_format = 0
			for i in contents:
				if "Birth:" in i:
					item['birthdate'], item['deathdate'], item['description'], item['burial'], item['plot'] = parsing_html(i)
					wrong_format = 1

			if wrong_format == 0:
				print "-------------------------------"
				print "-------------------------------"
				print "-------------------------------"
				# details = response.xpath('//*[@colspan="2"]').extract()[16]
				# item['description'] = parsing_tag(details)
				itme = None
			if 'Austin' not in item['burial']:
				item = None
			print "\n\n---------------------------------------------------"

		else:
			item = None



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