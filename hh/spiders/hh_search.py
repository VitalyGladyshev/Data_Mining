# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class HhSearchSpider(scrapy.Spider):
    name = 'hh_search'
    allowed_domains = ['nn.hh.ru']
    start_urls = ['https://nn.hh.ru/search/vacancy?only_with_salary=false&clusters=true&area=66&enable_snippets=true'
                  '&salary=&st=searchVacancy&text=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82']

    def parse(self, response):
        pagess = response.css('span.g-user-content a::attr(href)').extract()
        for itm in pagess:
            yield response.follow(itm, callback=self.parse_vacancies_page)
        pagination = response.css('a.bloko-button.HH-Pager-Controls-Next::attr(href)').extract()
        next_link = pagination[-1]
        yield response.follow(next_link, callback=self.parse)

    def parse_vacancies_page(self, response: HtmlResponse):
        title = response.css('span.highlighted::text').extract()
        salary = response.css('p.vacancy-salary::text').extract()
        skills = response.css('span.Bloko-TagList-Text::text').extract()
        company_name = response.css('a.vacancy-company-name span::text').extract()
        company_link = response.css('a.vacancy-company-name::attr(href)').extract()
        # print(company_link)
        yield {'title': title[0],
               'company_name': company_name,
               'company_link': company_link,
               'skills': skills,
               'salary': salary}
