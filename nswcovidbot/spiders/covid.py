import arrow
import scrapy
import json
import itertools

from scrapy import signals

from nswcovidbot.items import DefaultItemLoader, VenueItem


class CovidSpider(scrapy.Spider):
    name = 'covid'
    allowed_domains = ['data.nsw.gov.au']
    start_urls = ['https://data.nsw.gov.au/data/dataset/0a52e6c1-bc0b-48af-8b45-d791a6d8e289/resource/f3a28eed-8c2a-437b-8ac1-2dab3cf760f9/download/covid-case-locations-20210716-2359.json']
    state_path = None
    state = {}

    def __init__(self, state_path='state.json'):
        try:
            self.state_path = state_path
            with open(state_path, 'rb') as f:
                self.state = json.load(f)
        except FileNotFoundError:
            self.state = {}

    '''
        find_new_venues takes a new_list of venues and compares it to a previously seen list, returning only those
        elements that exist in the new list
    '''
    @staticmethod
    def find_new_venues(new_list, old_list):
        new_venues = []
        for venue in new_list:
            if venue not in old_list:
                new_venues.append(venue)
        return new_venues

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CovidSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, reason):
        if reason != 'finished':
            # we got an error. don't write out state so we can try again
            return

        # write out state if we closed successfully.
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f)

    def parse(self, response):
        # Example: 'Last-Modified': [b'Fri, 16 Jul 2021 14:24:41 GMT']
        last_modified = arrow.get(str(response.headers.get('Last-Modified'), 'utf-8'), 'ddd, DD MMM YYYY HH:mm:ss ZZZ')
        if self.state and self.state.get('last_modified'):
            last_scrape = arrow.get(self.state.get('last_modified'))
            # nothing changed. skip
            if last_modified < last_scrape:
                return

        venues = response.json().get('data').get('monitor')
        # save last_modified state and response data
        venue_diff = self.find_new_venues(venues, self.state.get('last_response', []))
        self.state['last_modified'] = str(last_modified)
        self.state['last_response'] = venues

        for venue in venue_diff:
            venue_item = DefaultItemLoader(VenueItem())
            venue_item.add_value('venue', venue.get('Venue'))
            venue_item.add_value('address', venue.get('Address'))
            venue_item.add_value('suburb', venue.get('Suburb'))
            venue_item.add_value('date', venue.get('Date'))
            venue_item.add_value('time', venue.get('Time'))
            venue_item.add_value('alert', venue.get('Alert'))
            venue_item.add_value('lon', venue.get('Lon'))
            venue_item.add_value('lat', venue.get('Lat'))
            venue_item.add_value('last_updated', venue.get('Last updated date'))
            yield venue_item.load_item()

