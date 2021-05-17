from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Compose


def get_tag_data(data):
    data = data[0]
    data_out = {}
    for key, value in data.items():
        if not (isinstance(value, dict) or isinstance(value, list)):
            data_out.update({key: value})
    return data_out


def get_post_data(post_graphql):
    post_graphql = post_graphql[0]
    data_out = {}

    data_out.update({
        'id': post_graphql['node']['id'],
        'shortcode': post_graphql['node']['shortcode'],
        'owner': post_graphql['node']['owner']['id'],
        'photo': None if post_graphql['node']['is_video'] else post_graphql['node']['thumbnail_resources'][-1]['src'],
        'meta': post_graphql['node']
    })

    return data_out


class InstagramTegLoader(ItemLoader):
    default_item_class = dict
    data_in = Compose(get_tag_data)

    time_parse_out = TakeFirst()
    data_out = TakeFirst()


class InstagramPostLoaders(ItemLoader):
    default_item_class = dict

    data_in = Compose(get_post_data)

    time_parse_out = TakeFirst()
    data_out = TakeFirst()
