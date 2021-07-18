import os

BOT_NAME = 'nswcovidbot'

SPIDER_MODULES = ['nswcovidbot.spiders']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'nswcovidbot (+http://twitter.com/nswcovidbot)'

ROBOTSTXT_OBEY = True

POSTGRES_DB_URI = os.environ.get('POSTGRES_URI')

TWITTER_AUTH = {
    'consumer_key': os.environ.get('TWITTER_CONSUMER_KEY'),
    'consumer_secret': os.environ.get('TWITTER_CONSUMER_SECRET'),
    'access_token': os.environ.get('TWITTER_ACCESS_TOKEN'),
    'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
}

ITEM_PIPELINES = {
    'nswcovidbot.pipelines.SQLPipeline': 0,
    'nswcovidbot.pipelines.TwitterPipeline': 1,
}