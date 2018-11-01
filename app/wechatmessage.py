import logging
import copy

from app.fields import Field, StringField, IntegerField


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
                logger.debug(
                    'Found Field {}: {} ==> {}'.format(name, k, v))
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
        # TODO ???
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
    event_key = StringField("EventKey")


class BaseReply(WechatMessage):
    to_user_name = StringField("ToUserName")
    from_user_name = StringField("FromUserName")
    create_time = IntegerField("CreateTime")
    msg_type = StringField("MsgType")

    def render(self, **args):
        for k, v in args:
            self[k] = v

    def serialize(self):
        from app.utils import etree
        root = etree.Element("xml")
        for v in self.data.values():
            if isinstance(v, Field):
                root.append(
                    v.get_element(self[v.name])
                )

        return root


@register_msg("text")
class TextMessage(BaseMessage):
    content = StringField("Content")


@register_event("subscribe")
class SubscribeEvent(BaseEvent):
    pass


@register_reply("text")
class TextReply(BaseReply):
    content = StringField("Content")


class ReplyFactory:
    def __init__(self, msg, msg_type="text"):
        self.__msg = msg
        self.__rep = reply_mapping[msg_type]
        self.__render = {"MsgType": msg_type}

    def render(self, **args):
        import time

        logger.debug("Reply rendering. args: %s", args)

        self.__render["ToUserName"] = self.__msg.from_user_name
        self.__render["FromUserName"] = self.__msg.to_user_name
        self.__render["CreateTime"] = int(time.time())

        for k, v in self.__rep.__data__.items():
            if k in args.keys():
                self.__render[v.name] = args[k]
                break
            elif v.name in args.keys():
                self.__render[v.name] = args[v.name]

        logger.debug("Reply rendering. __render: %s", self.__render)
        return self.__rep(**self.__render)


def parse_wechat_message(xml):
    """
    """
    from app.utils import etree, etree_to_dict
    logger.debug("Msg could parse - Msg: %s / Event: %s", msg_mapping, event_mapping)
    xml = etree_to_dict(etree.fromstring(xml))
    msg_id = xml["MsgId"]
    msg_type = xml["MsgType"]
    if msg_type == "event":
        msg = event_mapping["EventKey"]
    else:
        msg = msg_mapping[msg_type](**xml)

    return msg_id, msg


def build_wechat_message(wechat_message):
    from app.utils import etree
    root = wechat_message.serialize()
    return etree.tostring(root, encoding="utf-8")
