import scrapy
import urllib
import requests
import re
from selenium import webdriver


class DmozItem(scrapy.Item):
	Location = scrapy.Field()
	Title = scrapy.Field()
	Description = scrapy.Field()
	Address = scrapy.Field()
	Compensation = scrapy.Field()
	Employment_type = scrapy.Field()
	Link = scrapy.Field()
	Email = scrapy.Field()
class DmozSpider(scrapy.Spider):
	name = "craig"
	page_numbers = 0
	start_urls = [
	'https://losangeles.craigslist.org/d/retail-wholesale/search/ret?s=0'
	]
	def __init__(self):
		self.driver = webdriver.Chrome('E:/PROJECT/scrapy_python/craigslist/craigslist/craigslist/spiders/chromedriver.exe')
	def parse(self, response):
		links = response.css('a.result-title').xpath("@href").extract()
		for link in links:
			yield scrapy.Request(link, callback=self.parse_attr)
		next_page = "https://losangeles.craigslist.org/d/retail-wholesale/search/ret?s="+str(DmozSpider.page_numbers)
		if DmozSpider.page_numbers<=1000:
			DmozSpider.page_numbers +=120
			yield response.follow(next_page,callback=self.parse)

	def parse_attr(self, response):
		self.driver.get(response.url)
		next = self.driver.find_elements_by_css_selector("button.reply-button")
		next[0].click()
		
		item = DmozItem()
		Link = response.url
		Title = response.css('h1 span span::text').extract()
		Location = response.css('h1 span small::text').extract()
		
		ll = response.css('p span b::text').extract()
		Compensation = ll[0]
		Employment_type = ll[1]
		Email = response.css('a.mailapp::text').extract()
		Address = response.css('div.mapaddress::text').extract()
		Location[0] = Location[0].replace(" (","")
		Location[0] = Location[0].replace(")","")
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
		
		item['Title'] = Title
		item['Location'] = Address
		item['Compensation'] = Compensation
		item['Employment_type'] = Employment_type
		item['Address'] = Location
		item['Description'] = text_list
		item['Link'] = Link
		item['Email'] = Email
		return item
	