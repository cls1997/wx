from flask import current_app
from app.extensions import wechat
from wechat import filters


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

    from app.api.wechat import upload_img
    from app.api.baidulbs import get_image

    img = get_image(message.location_x, message.location_y)
    img = upload_img(img)

    return message.reply_image(img)


# @wechat.register_filter(filters.event('location'))
# def event_location_handler(message):
#     from app.api.baidueagle import entity_create, entity_list, track_addpoint
#     wechat_user = message.FromUserName
#     if entity_list(wechat_user)['status'] == 3003:
#         entity_create(wechat_user)

#     track_addpoint(wechat_user, message.latitude, message.longitude, message.create_time)
