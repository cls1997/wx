from . import WechatMessage
from .fields import StringField, IntegerField

msg_mapping = {"event": None}


def register_msg(name):
    def register(cls):
        msg_mapping[name] = cls
        return cls

    return register


class BaseMessage(WechatMessage):
    to_user_name = StringField("ToUserName")
    from_user_name = StringField("FromUserName")
    create_time = IntegerField("CreateTime")
    msg_type = StringField("MsgType")
    msg_id = IntegerField("MsgId")


@register_msg("text")
class TextMessage(BaseMessage):
    content = StringField("Content")


@register_msg("image")
class ImageMessage(BaseMessage):
    media_id = StringField("MediaId")
    pic_url = StringField("PicUrl")


@register_msg("voice")
class VoiceMessage(BaseMessage):
    media_id = StringField("MediaId")
    format = StringField("Format")


@register_msg("video")
class VideoMessage(BaseMessage):
    media_id = StringField("MediaId")
    thumb_media_id = StringField("ThumbMediaId")


@register_msg("shortvideo")
class ShortVideoMessage(BaseMessage):
    media_id = StringField("MediaId")
    thumb_media_id = StringField("ThumbMediaId")


@register_msg("location")
class LocationMessage(BaseMessage):
    location_x = IntegerField("Location_X")
    location_y = IntegerField("Location_Y")
    scale = IntegerField("Scale")
    label = StringField("Label")


@register_msg("link")
class LinkMessage(BaseMessage):
    title = StringField("Title")
    description = StringField("Description")
    url = StringField("Url")
