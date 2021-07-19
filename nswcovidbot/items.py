import scrapy
from scrapy.loader import ItemLoader

from itemloaders.processors import TakeFirst, MapCompose


def str_encode(value: str) -> str:
    return value.encode('ascii', 'ignore').decode('utf-8')

class DefaultItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip, str_encode)
    default_output_processor = TakeFirst()


class VenueItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    venue = scrapy.Field()
    address = scrapy.Field()
    suburb = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    alert = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    last_updated = scrapy.Field()
