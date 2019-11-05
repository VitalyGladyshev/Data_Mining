# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from scrapy.loader import ItemLoader
from hh.items import ZillowLoader
import os


class ZillowSpider(scrapy.Spider):
    # dir = ""  # os.curdir
    # path = os.path.join(dir, "geckodriver.exe")
    name = 'zillow'
    allowed_domains = ['zillow.com', 'photos.zillowstatic.com', 'zillowstatic.com']
    start_urls = ['https://www.zillow.com/fort-worth-tx/']
    browser = webdriver.Chrome("C:\\Projects\\Data_Mining\\chromedriver.exe")  # browser = webdriver.Firefox(path)  # browser = webdriver.Edge("C:\\Projects\\Data_Mining\\msedgedriver.exe")

    def parse(self, response: HtmlResponse):
        next = response.css('.zsg-pagination-next a::attr(href)').extract_first()
        yield response.follow(next, callback=self.parse)
        real_estate_list = response.css(
            'div#grid-search-results ul.photo-cards li article a.list-card-link::attr(href)'
        )
        for adv in real_estate_list.extract():
            yield response.follow(adv, callback=self.pars_adv)

    def pars_adv(self, response: HtmlResponse):
        self.browser.get(response.url)
        media = self.browser.find_element_by_css_selector('.ds-media-col')
        # media = self.browser.find_element_by_xpath('//div[contains(@class, "ds-media-col")]')
        # media = self.browser.find_element_by_xpath('//ul[@class="media-stream"]')
        photo_pic_img_len = len(self.browser.find_element_by_xpath(
            '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]').get_attribute("srcset").split(' ')[-2])
        print(1)
        while True:
            # media.send_keys(Keys.PAGE_DOWN)  # media.send_keys(Keys.ARROW_DOWN)
            # media.send_keys(Keys.PAGE_DOWN)
            # media.send_keys(Keys.PAGE_DOWN)
            # media.send_keys(Keys.PAGE_DOWN)
            # media.send_keys(Keys.PAGE_DOWN)
            # time.sleep(2)
            tmp_len = len(self.browser.find_element_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'
            ).get_attribute("srcset").split(' ')[-2])
            if photo_pic_img_len == tmp_len:
                break
            photo_pic_img_len = len(self.browser.find_element_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'
            ).get_attribute("srcset").split(' ')[-2])
        # images = [itm.get_attribute('srcset').split(' ')[-2] for itm in
        #           self.browser.find_element_by_xpath(
        #               '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')]
        # im = self.browser.find_element_by_xpath(
        #                 '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'
        #                 )

        title_list = response.xpath('//h1[@class="ds-address-container"]/span/text()').extract()
        price = response.xpath('//h3[@class="ds-price"]/span/span[@class="ds-value"]/text()').extract_first()
        perams_list = response.xpath('//ul[@class="ds-home-fact-list"]//span/text()').extract()
        image = self.browser.find_element_by_xpath(
                        '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'
                        ).get_attribute("srcset").split(' ')[-2]

        addition_item = ItemLoader(ZillowLoader(), response)
        addition_item.add_value('title', title_list)
        addition_item.add_value('price', price)
        addition_item.add_value('image', image)
        addition_item.add_value('params', perams_list)
        addition_item.add_value('url', response.url)

    def __del__(self):
        self.browser.close()

# browser.get('https://geekbrains.ru')
# field_mail = browser.find_element_by_xpath('//form[@class="registration-form-v2"]//input[@type="email"]')
# field_mail.send_keys('viv232@yandex.ru')
# field_password = browser.find_element_by_xpath('//form[@class="registration-form-v2"]//input[@type="password"]')
# field_password.send_keys('11111111')
# field_password.send_keys(Keys.ENTER)
# browser.get_cookies()
# sel_mail = '//form[@class="registration-form-v2"]//input[@type="email"]'
# browser.find_element_by_xpath(sel_mail).send_keys('1111')
# button = browser.find_element_by_xpath('//form[@class="registration-form-v2"]//button[@type="submit"]')
# button.click()
# # button = browser.find_element_by_xpath('//form[@class="registration-form-v2"]//button[@type="submit"][2]')
# slogan = browser.find_element_by_xpath('//div[@class="slogan-block"]')
# slogan.text
# slogan.find_element_by_xpath('//h1').text
# browser.window_handles
# browser.current_window_handle
# browser.switch_to_window('92AD40C6-AEE3-431D-A243-734E6072D518')
# browser.switch_to.window('EE4EA99F-47E2-4B8A-9672-80FD31DCD08A')
# browser.title
# browser.current_url
# body.send_keys(Keys.PAGE_DOWN)
# html = browser.find_element_by_xpath('html')
# html.send_keys(Keys.PAGE_UP)
# html.send_keys(Keys.ARROW_DOWN)
# html.send_keys(Keys.COMMAND + 'a')
# self.browser.close()
