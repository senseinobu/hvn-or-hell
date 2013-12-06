# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from hvnrhell.models import Term, Page, TermValue

class HeavenItem(Item):
    host = Field()
    url = Field()
    rating = Field()
    tokens = Field()

class TermItem(DjangoItem):
    django_model = Term

class PageItem(DjangoItem):
    django_model = Page
    tokens = Field()
    
class TermValueItem(DjangoItem):
    django_model = TermValue
