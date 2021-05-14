import scrapy
from ..xpath_selectors import xpath_selectors, xpath_data_selectors
from ..loaders import AvitoLoader


class AvitoParseSpider(scrapy.Spider):
    name = 'avito_parse'
    allowed_domains = ['www.avito.ru']
    start_urls = ['https://www.avito.ru/sankt-peterburg/kvartiry/prodam/']

    def _get_follow(self, response, selector_str, callback):
        for itm in response.xpath(selector_str):
            yield response.follow(itm, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response, xpath_selectors["pages"], self.parse
        )
        yield from self._get_follow(
            response, xpath_selectors["flat"], self.flat_parse,
        )

    def flat_parse(self, response):
        loader = AvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in xpath_data_selectors.items():
            loader.add_xpath(key, xpath)
