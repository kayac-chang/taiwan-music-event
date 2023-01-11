from decouple import config

BOT_NAME = 'event'
SPIDER_MODULES = ['event.spiders']
NEWSPIDER_MODULE = 'event.spiders'
ROBOTSTXT_OBEY = True
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

FEED_EXPORT_ENCODING = 'utf-8'


PG_HOST: str = config('PG_HOST')
PG_DBNAME: str = config('PG_DBNAME')
PG_USER: str = config('PG_USER')
PG_PASSWORD: str = config('PG_PASSWORD')
PG_PORT: int = config('PG_PORT', default=5432, cast=int)
ITEM_PIPELINES = {
    'event.pipelines.PGPipeline': 300,
}
