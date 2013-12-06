from stemming.porter2 import stem
from heaven.items import PageItem
from nltk.corpus import stopwords
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
    swords = stopwords.words('english')
    tokens = [token for token in tokens if token not in swords]
	return [stem(token) for token in tokens]

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

class HellSpider(CrawlSpider):
	name = "hell"
	start_urls = [#"http://reddit.com/r/nsfw",
		"http://porn.com",
		#"http://literotica.com",
		#"http://4chan.org",
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
		item = PageItem()
		item['hostname'] = hostname
		item['url'] = response.url
		item['tokens'] = tokenize(text)
		item['rating'] = 'R'
		return item
