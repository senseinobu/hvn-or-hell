#Run the crawler for the specified domain
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from PageGetter.spiders.lonespider import LoneSpider
from scrapy.utils.project import get_project_settings
def getPage():
    spider = LoneSpider()
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop,signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()

if __name__ == '__main__':
    getPage()
