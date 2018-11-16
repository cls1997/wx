import logging
import copy

from app.fields import Field, StringField, IntegerField, FloatField, ImageField


logger = logging.getLogger("WechatAPI")

msg_mapping = {"event": None}
event_mapping = {}
reply_mapping = {}


def register_msg(name):
    def register(cls):
        msg_mapping[name] = cls
        return cls
    return register


def register_event(name):
    def register(cls):
        event_mapping[name] = cls
        return cls
    return register


def register_reply(name):
    def register(cls):
        reply_mapping[name] = cls
        return cls
    return register


class WechatMessageMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name in ["WechatMessage", ]:
            return type.__new__(cls, name, bases, attrs)
        data = {}
        tmp_attrs = copy.deepcopy(attrs)
        for base in bases:
            if hasattr(base, '__data__'):
                tmp_attrs.update(copy.deepcopy(base.__data__))
        for k, v in tmp_attrs.items():
            if isinstance(v, Field):
                # logger.debug(
                #     'Found Field {}: {} ==> {}'.format(name, k, v))
                data[k] = v
                if k in attrs:
                    attrs.pop(k)

        logger.debug("Entity %s(%s)'s attributes: %s", name,
                     cls, [k for k in data.keys()])
        cls = type.__new__(cls, name, bases, attrs)
        cls.__data__ = data
        return cls


class WechatMessage(dict, metaclass=WechatMessageMetaclass):
    def __init__(self, **args):
        logger.debug("Message initializing .%s %s %s", self.__class__,
                     [v.name for v in self.data.values()],
                     [v for v in args.values()]
                     )
        if len(args) != len(self.data):
            raise TypeError("{} takes exactly {} argument ({} given)".format(
                self.__class__.__name__, len(self.data), len(args)))
        for k, v in self.data.items():
            try:
                self[k] = args[v.name]
            except KeyError:
                raise TypeError(
                    "'{}' has no attribute '{}({})'".format(self.__class__, k, v.name))
        super().__init__(args)

    def __getattr__(self, key):
        if key in self.data.keys():
            key = self.data[key].name
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (self.__class__, key))

    def __setattr__(self, key, value):
        # TODO Type judge
        logger.debug("self data: %s", self.data)
        for v in self.data.values():
            print(v.value, key)
            if v.value == key:
                print("QWE")
        self[key] = value

    @property
    def data(self):
        return self.__class__.__data__


class BaseMessage(WechatMessage):
    to_user_name = StringField("ToUserName")
    from_user_name = StringField("FromUserName")
    create_time = IntegerField("CreateTime")
    msg_type = StringField("MsgType")
    msg_id = IntegerField("MsgId")


class BaseEvent(WechatMessage):
    to_user_name = StringField("ToUserName")
    from_user_name = StringField("FromUserName")
    create_time = IntegerField("CreateTime")
    msg_type = StringField("MsgType")
    event = StringField("Event")


class BaseReply(WechatMessage):
    to_user_name = StringField("ToUserName")
    from_user_name = StringField("FromUserName")
    create_time = IntegerField("CreateTime")
    msg_type = StringField("MsgType")

    def serialize(self):
        from app.utils import etree
        root = etree.Element("xml")
        for v in self.data.values():
            if isinstance(v, Field) and self[v.name]:
                root.append(
                    v.get_element(self[v.name])
                )

        return root


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


@register_event("subscribe")
class SubscribeEvent(BaseEvent):
    pass


@register_event("unsubscribe")
class UnsubscribeEvent(BaseEvent):
    pass


@register_event("click")
class ClickEvent(BaseEvent):
    event_key = StringField("EventKey")

@register_event("LOCATION")
class LocationEvent(BaseEvent):
    latitude = FloatField("Latitude")
    longitude = FloatField("Longitude")
    precision = FloatField("Precision")



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


def parse_wechat_message(xml):
    """
    """
    from app.utils import etree, etree_to_dict
    logger.debug("Msg could parse - Msg: %s / Event: %s",
                 msg_mapping, event_mapping)
    xml = etree_to_dict(etree.fromstring(xml))
    msg_type = xml["MsgType"]
    if msg_type == "event":
        msg = event_mapping["Event"]
    else:
        try:
            msg = msg_mapping[msg_type](**xml)
        except KeyError:
            raise RuntimeError("Unsupported Message. %s", msg_type)
    return msg


def build_wechat_reply(msg, msg_type, response):
    import time
    from app.utils import etree

    reply_generator = reply_mapping[msg_type]

    logger.debug("Reply rendering. args: %s", response)
    response["ToUserName"] = msg.from_user_name
    response["FromUserName"] = msg.to_user_name
    response["CreateTime"] = int(time.time())
    response["MsgType"] = msg_type

    accept_key = []
    accept_key.extend([v.name for v in reply_generator.__data__.values()])
    accept_key.extend([k for k in reply_generator.__data__.keys()])
    tmp_key = [k for k in response.keys()]
    for k in tmp_key:
        if k not in accept_key:
            response.pop(k)

    for v in reply_generator.__data__.values():
        if v.name not in response.keys():
            response[v.name] = None

    wechat_message = reply_generator(**response)

    root = wechat_message.serialize()
    return etree.tostring(root, encoding="utf-8")
