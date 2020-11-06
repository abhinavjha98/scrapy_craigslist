import scrapy
import urllib
import requests
import re
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException

class DmozItem(scrapy.Item):
	Location = scrapy.Field()
	Title = scrapy.Field()
	Description = scrapy.Field()
	Address = scrapy.Field()
	Compensation = scrapy.Field()
	Employment_type = scrapy.Field()
	Link = scrapy.Field()
	Email = scrapy.Field()
	Name = scrapy.Field()
	Email = scrapy.Field()
class DmozSpider(scrapy.Spider):
	name = "craig"
	page_numbers = 120
	start_urls = [
	'https://minneapolis.craigslist.org/d/services/search/bbb'
	]
	def __init__(self):
		self.driver = webdriver.Chrome('E:/PROJECT/scrapy_python/craigslist/craigslist/chromedriver.exe')
	def parse(self, response):
		links = response.css('a.result-title').xpath("@href").extract()
		for link in links:
			yield scrapy.Request(link, callback=self.parse_attr)
		# next_page = "https://minneapolis.craigslist.org/search/bbb?s="+str(DmozSpider.page_numbers)
		# if DmozSpider.page_numbers<=6000:
		# 	DmozSpider.page_numbers +=120
		# 	yield response.follow(next_page,callback=self.parse)
		next_page = response.css('a.button.next').xpath("@href").extract()
		if next_page:
			next_href = next_page[0]
			next_page_url = 'https://minneapolis.craigslist.org' + next_href
			request = scrapy.Request(url=next_page_url)
			yield request

	def parse_attr(self, response):
		# self.driver.get(response.url)
		# try:
		# 	next = self.driver.find_elements_by_css_selector("button.reply-button")
		# 	next[0].click()
		# 	time.sleep(2)
		# except NoSuchElementException:
		# 	next=""

		item = DmozItem()

		# try:
		# 	next1 = self.driver.find_element_by_css_selector("div aside ul li p")
		# 	Name = next1.text
		# except NoSuchElementException:
		# 	Name = ""

		# try:
		# 	next2 = self.driver.find_element_by_css_selector("a.mailapp")
		# 	Email = next2.text
		# except NoSuchElementException:
		# 	Email = ""
		# if "@" in Name:
		# 	Name=""	
		Link = response.url
		Title = response.css('h1 span span::text').extract()
		Location = response.css('h1 span small::text').extract()
		
		ll = response.css('p span b::text').extract()
		if not ll:
			return
		else:
			Compensation = ll[0]
			try:
				Employment_type = ll[1] 
			except IndexError:
				Employment_type = ""
		Address = response.css('div.mapaddress::text').extract()
		try:
			Location[0] = Location[0].replace(" (","")
			Location[0] = Location[0].replace(")","")
		except IndexError:
			Location=""	
		Description = response.xpath("//section[@id='postingbody']/descendant::text()").extract()
		res=[]
		
		Description[0] = ""
		Description[1] = ""
		Description[2] = ""
		Description[3] = ""
		Description[4] = ""
		Description[5] = ""
		# Description[6] = ""
		for sub in Description: 
			res.append(re.sub('\n', '', sub))
		print(res)
		text_list=""
		for text in res:
			text = text.replace(",","")
			text_list = text_list+text
		# for text in Description:
		# 	text = text.rstrip("\n")
		# 	text_list=text_list+text
		# text_list = text_list.rstrip("\n")
		item['Name'] = ""
		item['Title'] = Title
		item['Location'] = Address
		item['Compensation'] = Compensation
		item['Employment_type'] = Employment_type
		item['Address'] = Location
		item['Description'] = text_list
		item['Link'] = Link
		item['Email'] = ""
		return item
	