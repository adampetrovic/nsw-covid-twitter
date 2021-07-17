# Define your item pipelines herec
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import tweepy


class TwitterPipeline:

    def __init__(self, creds):
        auth = tweepy.OAuthHandler(
            creds.get('consumer_key'),
            creds.get('consumer_secret'),
        )
        auth.set_access_token(
            creds.get('access_token'),
            creds.get('access_token_secret'),
        )
        self.twitter = tweepy.API(auth)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            creds=crawler.settings.get('TWITTER_AUTH'),
        )

    def process_item(self, item, spider):
        message = """
NEW EXPOSURE SITE IN NSW

Venue: {venue}
Address: {address}, {suburb}

Date: {date} 
Time: {time}

{advice}
        """
        status = self.twitter.update_status(
            status=message.format(
                venue=item.get('venue'),
                date=item.get('date'),
                time=item.get('time'),
                address=item.get('address'),
                suburb=item.get('suburb'),
                advice=item.get('alert'),
            ),
        )
        return item
