import scrapy
import urllib
import requests
import re
from selenium import webdriver

class DmozItem(scrapy.Item):
	Location = scrapy.Field()
class DmozSpider(scrapy.Spider):
	name = "craigs"
	page_numbers = 0
	start_urls = [
	'https://losangeles.craigslist.org/sgv/ret/d/fullerton-production-assemblers/7219026196.html'
	]
	def __init__(self):
		self.driver = webdriver.Chrome('E:/PROJECT/scrapy_python/craigslist/craigslist/craigslist/spiders/chromedriver.exe')
	def parse(self, response):
		yield scrapy.Request('https://losangeles.craigslist.org/sgv/ret/d/fullerton-production-assemblers/7219026196.html', callback=self.parse_attr)
	def parse_attr(self,response):
		self.driver.get(response.url)
		next = self.driver.find_elements_by_css_selector("button.reply-button")
		next[0].click()
		elems = self.driver.find_elements_by_xpath("//a[@href]")
		for elem in elems:
			print(elem.get_attribute("href"))