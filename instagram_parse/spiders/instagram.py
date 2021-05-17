import datetime
import json
import datetime as dt
from ..items import InstagramTagItem, InstagramPostItem
from ..loaders import InstagramTegLoader, InstagramPostLoaders
import scrapy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/accounts/login/']
    _login_url = "https://www.instagram.com/accounts/login/ajax/"
    _tags_path = "/explore/tags/"
    api_url = "/graphql/query/"
    query_hash = '9b498c08113f1e09617a1703c22b2f32'

    header_var = {
        'first': 10
    }

    def __init__(self, login, password, tags, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login = login
        self.password = password
        self.tags = tags

    def parse(self, response, *args, **kwargs):
        print(1)
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self._login_url,
                method="POST",
                callback=self.parse,
                formdata={"username": self.login, "enc_password": self.password, },
                headers={"X-CSRFToken": js_data["config"]["csrf_token"]},
            )
        except AttributeError as e:
            print(e)
            if response.json()["authenticated"]:
                for tag in self.tags:
                    yield response.follow(f"{self._tags_path}{tag}/", callback=self.tag_page_parse)

    def tag_page_parse(self, response):
        data = self.js_data_extract(response)
        content = data['entry_data']['TagPage'][0]['graphql']['hashtag']
        tag_item = InstagramTagItem()
        loader = InstagramTegLoader(tag_item)
        loader.add_value('time_parse', dt.datetime.now())
        loader.add_value('data', content)
        yield loader.load_item()

        for page_content in content['edge_hashtag_to_media']['edges']:
            yield from self.post_parse(page_content)

        self.header_var.update({
            'tag_name': content['name'],
            'after': content["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        })

        yield response.follow(
            f"{self.api_url}?query_hash={self.query_hash}&variables={json.dumps(self.header_var)}",
            callback=self.pagination_parse)

    def pagination_parse(self, response):
        data = response.json()

        for edge in data['data']['hashtag']['edge_hashtag_to_media']['edges']:
            yield from self.post_parse(edge)

        self.header_var.update({
            'tag_name': data['data']['hashtag']['name'],
            'after': data['data']['hashtag']["edge_hashtag_to_media"]["page_info"]["end_cursor"]
        })

        yield response.follow(
            f"{self.api_url}?query_hash={self.query_hash}&variables={json.dumps(self.header_var)}",
            callback=self.pagination_parse)

    def post_parse(self, data):
        post_item = InstagramPostItem()
        post_loader = InstagramPostLoaders(post_item)
        post_loader.add_value('time_parse', datetime.datetime.now())
        post_loader.add_value('data', data)
        yield post_loader.load_item()

    def js_data_extract(self, response):
        script = response.xpath(
            "//script[contains(text(), 'window._sharedData = ')]/text()"
        ).extract_first()
        return json.loads(script.replace("window._sharedData = ", "")[:-1])
