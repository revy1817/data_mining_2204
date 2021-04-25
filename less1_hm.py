import json
import time
from pathlib import Path
import requests


class Parse5ka:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    params = {
        "records_per_page": 12,
    }

    def __init__(self, star_url: str, cat_url: str, save_path: Path):
        self.star_url = star_url
        self.cat_url = cat_url
        self.save_path = save_path

    def _get_response(self, url, *args, **kwargs):
        while True:
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            time.sleep(3)

    def run(self):
        for product in self._parse(self.star_url, self.cat_url):
            file_path = self.save_path.joinpath(f"{product['group_id']}.json")
            self._save(product, file_path)

    def _parse(self, url: str, cat_url: str):
        while url:
            time.sleep(0.1)
            response = self._get_response(url, headers=self.headers, params=self.params)
            data = response.json()
            for cat in data:

                product = []
                cat_id = cat['parent_group_code']
                cat_name = cat['parent_group_name']

                cat_products = {
                    'group_id': cat_id,
                    'cat_name': cat_name,
                    'products': product
                }

                page = 1
                marker = True
                while marker:  # next выглядело как https://monolith/ и для получения данных используется метод замены
                    # значений айди категорий (который предварительно выгружался) и страниц в зависимости пустой ли Next
                    params_cat = {'categories': cat_id, 'page': page, "records_per_page": 12}
                    cat_response = self._get_response(cat_url, headers=self.headers, params=params_cat)
                    data_cat = cat_response.json()

                    if data_cat['next'] is None:
                        marker = False
                    else:
                        page += 1

                    for product_cat in data_cat['results']:
                        product.append(product_cat['name'])
                yield cat_products
            break

    def _save(self, data: dict, file_path):
        file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


if __name__ == "__main__":
    save_path = get_save_path("products")
    url = "https://5ka.ru/api/v2/categories/"
    url_cat = 'https://5ka.ru/api/v2/special_offers/?store=&records_per_page=12&page=1&categories=716&ordering=&price_promo__gte=&price_promo__lte=&search='
    parser = Parse5ka(star_url=url, cat_url=url_cat, save_path=save_path)
    parser.run()
