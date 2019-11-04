# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from bs4 import BeautifulSoup
from lxml.cssselect import CSSSelector
from scrapy.http import HtmlResponse
from lxml import html

def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def get_params(values):
    params = BeautifulSoup(values, 'html.parser').text
    values = {params.split(':')[0]:params.split(':')[1]}
    return values

def str_to_int(values):
    return int(values)

class AvitoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    title = scrapy.Field(output_processor=TakeFirst())

    auto_price_amount = scrapy.Field(input_processor=MapCompose(str_to_int), output_processor=TakeFirst())
    auto_price_currency = scrapy.Field(output_processor=TakeFirst())

    auto_description = scrapy.Field(output_processor=TakeFirst())
    auto_params = scrapy.Field(input_processor=MapCompose(get_params))
    auto_advanced_params = scrapy.Field(output_processor=TakeFirst())

    pass
