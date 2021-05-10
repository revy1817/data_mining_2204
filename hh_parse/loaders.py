from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose


def get_company(data):
    author = "https://hh.ru" + data
    return author


def get_salary(data):
    salary = data.replace("\xa0", "")
    return salary


def get_title(data):
    title = "".join(itm for itm in data if itm != " ")
    return title


def get_activity(data):
    activity = "".join(data).split(sep=', ')
    return activity


class VacancyLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_in = Join("")
    title_out = TakeFirst()
    salary_in = MapCompose(get_salary)
    salary_out = Join("")
    description_in = Join("")
    description_out = TakeFirst()
    company_in = MapCompose(get_company)
    company_out = TakeFirst()


class AuthorLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_in = Compose(get_title)
    title_out = TakeFirst()
    website_out = TakeFirst()
    activity_out = MapCompose(get_activity)
    description_in = Join("")
    description_out = TakeFirst()
