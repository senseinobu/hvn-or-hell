from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from heaven.spiders.heaven_spider import HeavenSpider
from scrapy.utils.project import get_project_settings

spider = HeavenSpider()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop,signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run()
