# Scrapy settings for heaven project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'heaven'

SPIDER_MODULES = ['heaven.spiders']
NEWSPIDER_MODULE = 'heaven.spiders'

ITEM_PIPELINES = {
    'heaven.pipelines.TrainingPipeline':1000,
}

AUTOTHROTTLE_ENABLED = True
CONCURRENT_REQUESTS_PER_DOMAIN = 2

ROBOTSTXT_OBEY = True
DEPTH_LIMIT = 2

LOG_ENABLED = False

import sys
sys.path.insert(0, '/home/senseinobu/HeavenOrHell/site470')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'site470.settings'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'heaven (+http://www.yourdomain.com)'
