import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from yellow.items import YellowItem
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

class YellowSpider(CrawlSpider):
	name = 'yellow'
	allowed_domains = ['yellow.co.nz']
	# rules = (Rule(LxmlLinkExtractor(allow=(r'\/([A-Z])([A-Z0-9]{9})'),deny=('')),callback='parse_item'),Rule(LxmlLinkExtractor(allow=(''))),),)

	rules = (Rule(LxmlLinkExtractor(allow=(r'https://yellow.co.nz/canterbury-region/plumbers/page/.*',r'.*what=plumbers&where=Canterbury+Region.*')), follow=True,),
			 Rule(LxmlLinkExtractor(allow=(r'https://yellow.co.nz/y/.*'), deny=(r'.*more', r'.*Other')),callback='parse_business', follow=False,),
			 Rule(LxmlLinkExtractor(allow=('')), follow=False,))

	def __init__(self,*args, **kwargs):
		super(YellowSpider, self).__init__(*args, **kwargs)
		start_url='https://yellow.co.nz/canterbury-region/plumbers/page/1?what=plumbers&where=Canterbury+Region'
		self.start_urls = [start_url]
	

	def parse_business(self,response):
		item = YellowItem()
		print "\n\n---------------------START-----------------------"
		print "\n\n---------------------START-----------------------"
		print "\n\n---------------------START-----------------------"
		print response.url
		item["Company"] = response.xpath('//*[@id="businessDetailsPrimary"]/div[1]/div[3]/h1/span').extract()
		item["PhoneNumber"] = response.xpath('//*[@id="businessDetailsPrimary"]/div[2]/div/span[1]/a[1]').extract()
		item["MailingAddress"] = response.xpath('//*[@id="detailSectionSecondary"]/div[2]/section[3]/div[2]/p').extract()
		item["email"] = response.xpath('//*[@id="businessDetailsPrimary"]/div[2]/div/meta').extract()
		item["url"] = response.url
		print item
		yield item

	def process_links(self,links):
		print "\n       LINKS"
		links_list = []
		for i in links:
			if "https://www.tripadvisor.com/Attraction_Review" in i.url:
				links_list.append(i)
				print i.url
		return links_list