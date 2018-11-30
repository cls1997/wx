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


@wechat.register_filter(filters.message.location)
def location_handler(message):
    # from app.api.baidueagle import entity_create, entity_list, track_addpoint

    # wechat_user = msg.FromUserName
    # if entity_list(wechat_user)['status'] == 3003:
    #     print(entity_create(wechat_user))

    # response = track_addpoint(
    #     wechat_user, msg.location_x, msg.location_y, msg.create_time)

    from app.api.baidulbs import get_image

    try:
        img = get_image(message.location_x, message.location_y)
        logger.debug(img)
        img_media_id = wechat.client.media.upload('image', ('a.png', img))
        return message.reply_image(img_media_id)
    except WechatAPIException as e:
        logger.exception(e)
        return message.reply_text("Service Error")

# @wechat.register_filter(filters.event('location'))
# def event_location_handler(message):
#     from app.api.baidueagle import entity_create, entity_list, track_addpoint
#     wechat_user = message.FromUserName
#     if entity_list(wechat_user)['status'] == 3003:
#         entity_create(wechat_user)

#     track_addpoint(wechat_user, message.latitude, message.longitude, message.create_time)

@wechat.register_filter(filters.message.startswith('geez'))
def geez(message):
    return message.reply_articles([
        {
            "Title":'title',
            "Description": 'desc',
            "PicUrl": 'url',
            "Url": 'http://120.79.186.46'
        }
    ])