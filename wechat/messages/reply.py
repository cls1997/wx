from . import WechatMessage
from .fields import Field, ImageField, IntegerField, StringField

reply_mapping = {}


def register_reply(name):
    def register(cls):
        reply_mapping[name] = cls
        return cls

    return register


class BaseReply(WechatMessage):
    to_user_name = StringField("ToUserName")
    from_user_name = StringField("FromUserName")
    create_time = IntegerField("CreateTime")
    msg_type = StringField("MsgType")

    def serialize(self):
        from .utils import etree
        root = etree.Element("xml")
        for v in self._field.values():
            if isinstance(v, Field) and self[v.name]:
                root.append(
                    v.get_element(self[v.name])
                )

        rv = etree.tostring(root, encoding="utf-8")
        return rv


@register_reply("text")
class TextReply(BaseReply):
    content = StringField("Content")


@register_reply("image")
class ImageReply(BaseReply):
    media_id = ImageField("MediaId")


@register_reply("voice")
class VoiceReply(BaseReply):
    media_id = StringField("MediaId")
    title = StringField("Title")
    description = StringField("Description")


@register_reply("music")
class MusicReply(BaseReply):
    title = StringField("Title")
    description = StringField("Description")
    music_url = StringField("MusicURL")
    hq_music_url = StringField("HQMusicUrl")
    thumb_media_id = StringField("ThumbMediaId")


class ArticlesReply(BaseReply):
    pass
