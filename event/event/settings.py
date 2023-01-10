
BOT_NAME = 'event'
SPIDER_MODULES = ['event.spiders']
NEWSPIDER_MODULE = 'event.spiders'
ROBOTSTXT_OBEY = True
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

FEED_EXPORT_ENCODING = 'utf-8'
