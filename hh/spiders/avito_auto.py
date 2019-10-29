# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from hh.items import AvitoRealAuto


class AvitoAutoSpider(scrapy.Spider):
    name = 'avito_auto'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/nizhniy_novgorod/avtomobili']

    def parse(self, response: HtmlResponse):  # response: HtmlResponse для отображения методов
        auto_pages = response.xpath('//a[contains(@class, "item-description-title-link")]/@href').extract()
        for itm in auto_pages:
            yield response.follow(itm, callback=self.parse_auto_page, cb_kwargs={'auto_url': itm})
        pagination = response.xpath('//a[contains(@class, "js-pagination-next")]/@href').extract_first()
        yield response.follow(pagination, callback=self.parse)

    def parse_auto_page(self, response: HtmlResponse, auto_url):
        addition_item = ItemLoader(AvitoRealAuto(), response)
        addition_item.add_xpath('title', '//h1[@class="title-info-title"]/span[@itemprop="name"]/text()')
        addition_item.add_xpath('price', '//div[@class="item-price"]//span[@class="js-item-price"]/@content')
        addition_item.add_xpath('photos', '//div[contains(@class, "js-gallery-img-frame")]/@data-url')
        addition_item.add_xpath('params', '//div[@class="item-params"]/ul[@class="item-params-list"]/li')
        addition_item.add_value('url', auto_url)
        yield addition_item.load_item()

        # name = response.xpath('//span[contains(@class, "title-info-title-text")]/text()').extract_first()
        # price = response.xpath('//span[contains(@class, "js-item-price")]/text()').extract_first()
        # address = response.xpath('//span[contains(@class, "item-address__string")]/text()').extract_first()
