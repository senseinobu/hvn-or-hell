from urlparse import urlparse
from stemming.porter2 import stem
from PageGetter.items import PageItem
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


#This is a spider set up to get only a single page. Set up for later things
class LoneSpider(CrawlSpider):
    name = "LoneSpider"
    rules = (
        Rule(SgmlLinkExtractor(), callback='parse_item'),
    )
    items = []
    
    def __init__(self, **kw):
        super(LoneSpider, self).__init__(**kw)
        url = kw.get('url') or kw.get('domain') or 'http://scrapinghub.com/'
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://%s/' % url
        self.url = url
        self.allowed_domains = [urlparse(url).hostname.lstrip('www.')]
           
    def parse_item(self, response):
        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

        text = lxml.html.tostring(root, encoding=unicode, method="text")
        hostname = response.url.split("/")[2]
        removeNonAscii(text)
        item = PageItem()
        item['host'] = hostname
        item['url']=response.url
        item['tokens'] = tokenize(text)
        item['rating'] = '?'
        return item
