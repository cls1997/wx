import logging
import copy
import types

from .fields import Field

logger = logging.getLogger("WechatAPI")

__all__ = ['WechatMessage', 'parse_wechat_message', 'create_reply']


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
        # TODO: Encrypt Message Handle
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
        # TODO: Type judge
        logger.debug("self data: %s", self.data)
        if (isinstance(value, types.FunctionType)):
            super().__setattr__(key, types.MethodType(value, self))
            return
        for v in self.data.values():
            if v.name == key:
                print("QWE")
        self[key] = value

    @property
    def data(self):
        return self.__class__.__data__


from .message import msg_mapping, BaseMessage
from .reply import reply_mapping, BaseReply
from .event import event_mapping, BaseEvent


def parse_wechat_message(xml)->BaseMessage:
    """
    Initail Message Object.
    Add some useful functions.
    """

    def _reply_text(self, content):
        return create_reply(self, 'text', {"Content": content})

    def _reply_media(media):
        def func(self, media_id, **kwargs):
            kwargs["media_id"] = media_id
            return create_reply(self, media, kwargs)
        return func

    def _reply_articles(self, articles):
        # TODO
        pass

    funcs = {
        "reply_text": _reply_text,
        "reply_image": _reply_media("image"),
        "reply_voice": _reply_media("voice"),
        "reply_video": _reply_media("video"),
        # "reply_articles": _reply_articles,
    }

    from .utils import etree, etree_to_dict
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
    for k, v in funcs.items():
        setattr(msg, k, v)
    return msg


def create_reply(msg: BaseMessage, msg_type: str, reply: dict)->BaseReply:
    """
    """
    import time

    reply_klz = reply_mapping[msg_type]

    logger.debug("Reply rendering. args: %s", reply)
    reply["ToUserName"] = msg.from_user_name
    reply["FromUserName"] = msg.to_user_name
    reply["CreateTime"] = int(time.time())
    reply["MsgType"] = msg_type

    accept_key = []
    accept_key.extend([v.name for v in reply_klz.__data__.values()])
    accept_key.extend([k for k in reply_klz.__data__.keys()])
    tmp_key = [k for k in reply.keys()]
    # Delete unacceptable keys
    for k in tmp_key:
        if k not in accept_key:
            reply.pop(k)

    for v in reply_klz.__data__.values():
        if v.name not in reply.keys():
            reply[v.name] = None

    wechat_message = reply_klz(**reply)
    return wechat_message
