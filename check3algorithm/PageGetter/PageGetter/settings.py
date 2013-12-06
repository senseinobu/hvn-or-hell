# Scrapy settings for PageGetter project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'PageGetter'

SPIDER_MODULES = ['PageGetter.spiders']
NEWSPIDER_MODULE = 'PageGetter.spiders'

ITEM_PIPELINES = {
    'PageGetter.pipelines.JsonExportPipeline':0,
}

AUTOTHROTTLE_ENABLED = True
CONCURRENT_REQUESTS_PER_DOMAIN = 2

ROBOTSTXT_OBEY = True
DEPTH_LIMIT = 1

#LOG_ENABLED = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'PageGetter (+http://www.yourdomain.com)'
