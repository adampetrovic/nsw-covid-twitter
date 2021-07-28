import logging
from datetime import datetime
from itertools import groupby
from operator import attrgetter

import tweepy
import arrow
from scrapy.exceptions import DropItem

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from nswcovidbot.models import Base, Venue, Tweet
from nswcovidbot.templates import AGGREGATE_TEMPLATE, CASE_TEMPLATE



class ValidationPipeline(object):

    def process_item(self, item, spider):
        required_keys = ['venue', 'suburb', 'date']
        for key in required_keys:
            if not item.get(key):
                raise DropItem('Missing required key / value on item: {}'.format(key))


class SQLPipeline(object):

    def __init__(self, db_uri):
        self.session = None
        self.engine = create_engine(db_uri)
        self.session_factory = sessionmaker(bind=self.engine)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_uri=crawler.settings.get('DB_URI')
        )

    def open_spider(self, spider):
        self.create_all()
        self.session = self.session_factory()

    def close_spider(self, spider):
        self.session.close()

    def create_all(self):
        Base.metadata.create_all(bind=self.engine)

    def process_item(self, item, spider):
        venue = self.session.query(Venue).filter_by(
            name=item.get('venue'),
            address=item.get('address'),
            suburb=item.get('suburb'),
            date=item.get('date'),
            time=item.get('time')
        ).first()

        if venue:
            raise DropItem("Venue already seen.")
        else:
            venue = Venue(
                name=item.get('venue'),
                address=item.get('address'),
                suburb=item.get('suburb'),
                date=item.get('date'),
                time=item.get('time'),
                alert=item.get('alert'),
                latitude=item.get('lat'),
                longitude=item.get('lon'),
                last_update=item.get('last_updated'),
            )
            try:
                self.session.add(venue)
                self.session.commit()
            except:
                self.session.rollback()
                raise DropItem("Couldn't save venue to database")

        return item


class TwitterPipeline:

    session = None

    def __init__(self, db_uri, creds):
        self.engine = create_engine(db_uri)
        self.session_factory = sessionmaker(bind=self.engine)

        auth = tweepy.OAuthHandler(
            creds.get('consumer_key'),
            creds.get('consumer_secret'),
        )
        auth.set_access_token(
            creds.get('access_token'),
            creds.get('access_token_secret'),
        )
        self.twitter = tweepy.API(auth)

    def open_spider(self, spider):
        self.session = self.session_factory()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_uri=crawler.settings.get('DB_URI'),
            creds=crawler.settings.get('TWITTER_AUTH'),
        )

    def close_spider(self, spider):
        # stopped scraping, make decision on what to do with the tweets
        self.aggregate_tweet()
        self.session.close()

    def aggregate_tweet(self):
        # find suburb breakdown we haven't tweeted about
        suburbs = self.session.query(Venue.suburb, func.count(func.distinct(Venue.name))) \
            .join(Tweet, Venue.tweet, isouter=True)\
            .filter_by(tweet_id=None)\
            .group_by(Venue.suburb)\
            .order_by(Venue.suburb)\
            .all()

        venues = self.session.query(Venue)\
            .join(Tweet, Venue.tweet, isouter=True)\
            .filter_by(tweet_id=None)\
            .order_by(Venue.suburb, Venue.date)\
            .all()

        if not suburbs or not venues:
            logging.info('no new venues found. quitting.')
            # nothing to post, exit
            return

        logging.info('{} new venues found. tweeting.'.format(len(venues)))

        # does a group by venue name, so we can collate it into a single tweet
        venue_group = [list(g) for k, g in groupby(venues, attrgetter('name', 'suburb'))]
        aggr_body = AGGREGATE_TEMPLATE.render(
            suburbs=suburbs,
            venue_count=len(venue_group),
            now=arrow.get(tzinfo='Australia/Sydney').format('ddd D/MMM h:mma'),
        )

        # aggregate tweet
        aggr_tweet = self.twitter.update_status(
            status=aggr_body,
        )

        for group in venue_group:
            dates = [(x.date, x.time) for x in group]
            venue_body = CASE_TEMPLATE.render(venue=group[0], dates=dates).strip()

            try:
                text = (venue_body[:277] + '...') if len(venue_body) > 280 else venue_body
                status = self.twitter.update_status(
                    status=text,
                    in_reply_to_status_id=aggr_tweet.id,
                )
            except tweepy.error.TweepError as e:
                logging.error("Couldn't post tweet.", e)
                continue

            logging.info('sending tweet. id={}'.format(status.id))
            for venue in group:
                venue.tweet = Tweet(
                    tweet_id=status.id,
                    venue_id=venue.id,
                )
                self.session.add(venue)
                self.session.commit()

    def process_item(self, item, spider):
        return item