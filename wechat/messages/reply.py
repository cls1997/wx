from . import WechatMessage
from .fields import Field, ImageField, IntegerField, StringField, ArticlesField

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

    @classmethod
    def accept_keys(cls):
        accept_keys = []
        accept_keys.extend([v.name for v in cls._fields.values()])
        accept_keys.extend([k for k in cls._fields.keys()])
        return accept_keys

    def serialize(self):
        from .utils import etree
        root = etree.Element("xml")
        for v in self._fields.values():
            value = getattr(self, v.name, None)
            if isinstance(v, Field) and value:
                root.append(
                    v.get_element(value)
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

@register_reply("news")
class ArticlesReply(BaseReply):
    article_count = IntegerField("ArticleCount")
    articles = ArticlesField("Articles")
