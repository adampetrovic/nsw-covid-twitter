from typing import List

import arrow
import scrapy
import json
import logging

from scrapy import signals

from nswcovidbot.items import DefaultItemLoader, VenueItem


class CovidSpider(scrapy.Spider):
    name = 'covid'
    allowed_domains = ['data.nsw.gov.au']
    start_urls = ['https://data.nsw.gov.au/data/dataset/0a52e6c1-bc0b-48af-8b45-d791a6d8e289/resource/f3a28eed-8c2a-437b-8ac1-2dab3cf760f9/download/covid-case-locations-20210716-2359.json']

    def parse(self, response):
        venues = response.json().get('data').get('monitor')
        for venue in venues:
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