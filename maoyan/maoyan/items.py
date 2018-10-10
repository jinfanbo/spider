# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class MaoyanItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nickName = Field()
    movieId = Field()
    score = Field()
    cityName = Field()
    content = Field()

