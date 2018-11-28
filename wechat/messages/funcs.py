# coding: utf8


import logging

from .event import event_mapping
from .message import msg_mapping, BaseMessage
from .reply import reply_mapping, BaseReply

logger = logging.getLogger("WechatAPI")


def parse_wechat_message(xml) -> BaseMessage:
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

    # def _reply_articles(self, articles):
    #     # TODO
    #     pass

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


def create_reply(msg: BaseMessage, msg_type: str, reply: dict) -> BaseReply:
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
