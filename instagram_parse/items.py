# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramTagItem(scrapy.Item):
    time_parse = scrapy.Field()
    data = scrapy.Field()


class InstagramPostItem(scrapy.Item):
    time_parse = scrapy.Field()
    data = scrapy.Field()
