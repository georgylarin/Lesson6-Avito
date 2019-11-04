# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avito.items import AvitoItem
from scrapy.loader import ItemLoader

class AvitoSpiderSpider(scrapy.Spider):
    name = 'avito_auto'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili/bmw/1?user=1']

    def parse(self, response):
        ads_link = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        for link in ads_link:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoItem(), response=response)
        loader.add_xpath('photos', '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')

        loader.add_css('auto_price_currency', 'meta[property="product:price:currency"]::attr(content)')
        loader.add_css('auto_price_amount', 'meta[property="product:price:amount"]::attr(content)')

        loader.add_css('auto_description', 'div.item-descpition-text > p::text')
        loader.add_css('auto_params', 'ul.item-params-list li')
        loader.add_css('auto_advanced_params', 'ul.advanced-params li')

        yield loader.load_item()