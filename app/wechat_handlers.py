import logging

from app.extensions import wechat
from wechat import filters
from wechat.client.exception import WechatAPIException

logger = logging.getLogger('flask.app')


@wechat.register_filter(filters.all)
def handler(message):
    return message.reply_text("Test")


@wechat.register_filter(filters.message.text)
def text_handler(message):
    return message.reply_text(message.content)


@wechat.register_filter(filters.message.startswith('geez'))
def geez(message):
    return message.reply_articles([
        {
            "Title": 'title',
            "Description": 'desc',
            "PicUrl": 'url',
            "Url": 'http://120.79.186.46/wxjs/'
        }
    ])


@wechat.register_filter(filters.message.startswith('#'))
def console_mode(message):
    content = message.content
    default_menu = {
        "button": [
            {
                "type": "view",
                "name": "词典",
                "url": "http://120.79.186.46/wxjs/"
            },
        ]
    }
    command = content[1:]

    funcs = {
        'delete': wechat.client.menu.delete,
        'add': lambda: wechat.client.menu.create(default_menu),
        'refresh_token': lambda: wechat.client.refresh_token()
    }
    try:
        func = funcs[command]
        res = func()
        print(res)
        return message.reply_text("ok\n result: {}".format(res))
    except KeyError:
        return message.reply_text('unknown command')
    except WechatAPIException:
        return message.reply_text('error')
