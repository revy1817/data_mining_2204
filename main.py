from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from avito.spiders.avito_parse import AvitoParseSpider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("avito.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(AvitoParseSpider)
    crawler_process.start()
