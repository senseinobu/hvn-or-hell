from stemming.porter2 import stem
from heaven.items import HeavenItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item
import lxml.etree
import lxml.html
import json
import re

def tokenize(text):
	tokens = re.findall("[\w']+", text.lower())
	return [stem(token) for token in tokens]

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

class HeavenSpider(CrawlSpider):
	name = "heaven"
	start_urls = [#"http://timeforkids.com",
		"http://nick.com",
		#"http://dogonews.com",
		#"http://theconnectedclassroom.wikispaces.com/News",
		#'http://washingtonpost.com/lifestyle/kidspost',
		#'http://news.nationalgeographic.com/news/',
		#'http://teacher.scholastic.com/activities/scholasticnews/index.html',
		#'http://funbrain.com',
		#'http://kidsites.com',
		#'http://www.brainpop.com'
	]
	allowed_domains = [url.split('/')[2] for url in start_urls]
	rules = (
		Rule(SgmlLinkExtractor(), callback='parse_item'),
	)
	items = []
	def parse_item(self, response):
		root = lxml.html.fromstring(response.body)
		lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

		text = lxml.html.tostring(root, encoding=unicode, method="text")
		hostname = response.url.split("/")[2]
		removeNonAscii(text)
		item = HeavenItem()
		item['host'] = hostname
		item['url']=response.url
		item['tokens'] = tokenize(text)
		item['rating'] = 'G'
		return item
