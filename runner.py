from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh import settings
# from hh.spiders.hh_search import HhSearchSpider
from hh.spiders.avito_realty import AvitoRealtySpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoRealtySpider)     # можно несколько пауков здесь добавить
    process.start()
