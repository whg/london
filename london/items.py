# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LondonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BoroughItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    borough = scrapy.Field()
