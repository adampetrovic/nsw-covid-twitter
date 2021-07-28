import os

BOT_NAME = 'nswcovidbot'

SPIDER_MODULES = ['nswcovidbot.spiders']

LOG_FORMATTER = 'nswcovidbot.middleware.LogFormatter'
LOG_LEVEL = 'INFO'
STATS_CLASS = 'scrapy.statscollectors.DummyStatsCollector'

USER_AGENT = 'nswcovidbot (+https://twitter.com/nswcovidbot)'

DB_URI = os.environ.get('DB_URI')

TWITTER_AUTH = {
    'consumer_key': os.environ.get('TWITTER_CONSUMER_KEY'),
    'consumer_secret': os.environ.get('TWITTER_CONSUMER_SECRET'),
    'access_token': os.environ.get('TWITTER_ACCESS_TOKEN'),
    'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
}

ITEM_PIPELINES = {
    'nswcovidbot.pipelines.ValidationPipeline': 0,
    'nswcovidbot.pipelines.SQLPipeline': 1,
    'nswcovidbot.pipelines.TwitterPipeline': 1,
}
