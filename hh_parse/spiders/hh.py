import scrapy

from .. import xpath_selectors as xp_s
from ..loaders import VacancyLoader, AuthorLoader


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def _get_follow(self, response, selector_str, callback):
        for itm in response.xpath(selector_str):
            yield response.follow(itm, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response, xp_s.xpath_selectors["vacancy"], self.vacancy_parse
        )
        yield from self._get_follow(
            response, xp_s.xpath_selectors["pagination"], self.parse
        )

    def vacancy_parse(self, response):
        loader = VacancyLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in xp_s.xpath_data_selectors.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
        yield from self._get_follow(
            response, xp_s.xpath_data_selectors['company'], self.company_parse
        )

    def company_parse(self, response):
        loader = AuthorLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in xp_s.xpath_company_data_selectors.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
