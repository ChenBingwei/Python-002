# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SmzdmTop10Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    shampoo_rank = scrapy.Field()
    shampoo_name = scrapy.Field()
    shampoo_evaluate = scrapy.Field()
    shampoo_comments = scrapy.Field()
