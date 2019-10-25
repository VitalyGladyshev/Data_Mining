# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class AvitoRealtySpider(scrapy.Spider):
    name = 'avito_realty'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/zhukovskiy/kvartiry']

    def parse(self, response: HtmlResponse):  # response: HtmlResponse для отображения методов
        kv_pages = response.xpath('//a[contains(@class, "item-description-title-link")]/@href').extract()
        for itm in kv_pages:
            yield response.follow(itm, callback=self.parse_kv_page, cb_kwargs={'kv_url': itm})
        pagination = response.xpath('//a[contains(@class, "js-pagination-next")]/@href').extract_first()
        yield response.follow(pagination, callback=self.parse)

    def parse_kv_page(self, response: HtmlResponse, kv_url):
        name = response.xpath('//span[contains(@class, "title-info-title-text")]/text()').extract_first()
        price = response.xpath('//span[contains(@class, "js-item-price")]/text()').extract_first()
        address = response.xpath('//span[contains(@class, "item-address__string")]/text()').extract_first()

        item = {'name': name,
                'url': kv_url,
                'price': price,
                'address': address}
        yield item

        # tag_keywords = response.xpath('//i[contains(@class, "i-tag")]/@keywords').extract_first()
        # tags = []
        # if tag_keywords:
        #     tag_attr_url = '/posts?tag='
        #     tags = [{'name': itm, 'url': f'{tag_attr_url}itm'} for itm in tag_keywords.split(', ')]

    #     yield response.follow(author, callback=self.creator_parse, cb_kwargs={'item': item})
    #
    # def creator_parse(self, response: HtmlResponse, item):
    #     item['author_name'] = response.xpath("//section[@id='main-content']//span[@class='h2']/text()").extract_first()
    #     item['author_age'] = response.xpath(
    #         "//section[@id='main-content']//span[@class='h5']/span/text()").extract_first()
    #     yield item
