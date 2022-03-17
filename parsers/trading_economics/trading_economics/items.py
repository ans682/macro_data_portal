# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TradingEconomicsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    country_name = scrapy.Field()
    last_value = scrapy.Field()
    prev_value = scrapy.Field()
    reference = scrapy.Field()
    units = scrapy.Field()
    
    test2 = scrapy.Field()
