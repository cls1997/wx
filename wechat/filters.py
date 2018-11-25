"""
source: https://github.com/Xavier-Lam/flask-wechat/blob/master/flask_wechat/filters.py
"""

from functools import reduce
import re
from .messages import WechatMessage

__all__ = ["all", "and_", "event", "message", "or_"]


def _typeof(t):
    return lambda m: m.msg_type == t


def _match(message, contains, accuracy=True, ignorecase=False):
    """帮助匹配文本的函数"""
    if ignorecase:
        message = message.lower()
        contains = contains.lower()
    if accuracy:
        return 0 if message == contains else -1
    else:
        return message.find(contains)


class Filter(object):
    def __call__(self, message):
        raise NotImplementedError()


class Event(Filter):
    def __call__(self, type=None):
        def decorated_func(message):
            rv = message.msg_type == "event"
            if rv and type:
                return message.event == type
            return rv
        if isinstance(type, WechatMessage):
            return type.msg_type == "event"
        return decorated_func

    # 订阅
    def subscribe(self, m): return self("subscribe")(m)

    # 取消订阅
    def unsubscribe(self, m): return self("unsubscribe")(m)

    # 点击
    def click(self, key=None):
        def decorated_func(message):
            rv = self("CLICK")(message)
            if rv and key:
                return message.eventkey == key
            return rv

        if isinstance(key, WechatMessage):
            return self("CLICK")(key)
        return decorated_func

    # 点击跳转
    def view(self, url=None, accuracy=False, ignorecase=False):
        def decorated_func(message):
            rv = self("VIEW")(message)
            if rv and url:
                return _match(message.eventkey, url, accuracy, ignorecase) >= 0
            return rv

        if isinstance(url, WechatMessage):
            return self("VIEW")(url)
        return decorated_func


class Message(Filter):
    def __call__(self, message):
        return message.msg_type != "event"

    
    typeof = staticmethod(_typeof)

    image = staticmethod(_typeof("image"))
    voice = staticmethod(_typeof("voice"))
    video = staticmethod(_typeof("video"))
    shortvideo = staticmethod(_typeof("shortvideo"))
    location = staticmethod(_typeof("location"))

    def contains(self, s, i=False): return \
        lambda m: self.text(m) and _match(m.content, s, False, i) >= 0

    # 开头
    def startswith(self, s, i=False): return \
        lambda m: self.text(m) and _match(m.content, s, False, i) == 0

    # # 正则
    # def regex(self, p, fl=0): return \
    #     lambda m: self.text() and not not re.match(p, m.content, fl)

    # # 文本在下列某种状况中
    # def in_(self, list, comparer=None):
    #     if not comparer:
    #         comparer = self.contains

    #     def func(message):
    #         for item in list:
    #             if comparer(item)(message):
    #                 return True
    #         return False
    #     return func

    # # 在下列正则中
    # def regex_in(self, patterns):
    #     def func(message):
    #         for pattern in patterns:
    #             if re.match(pattern, message):
    #                 return True
    #         return False
    #     return and_(self.text, func)

    def text(self, text=None, ignorecase=False):
        def decorated_func(message):
            rv = self.typeof("text")(message)
            if rv and text:
                return _match(message.content, text, True, ignorecase) >= 0
            return rv
        if isinstance(text, WechatMessage):
            return self.typeof("text")(text)
        return decorated_func

    # 在区域内
    def in_location(self, longitude, latitude, range):
        def decorated_func(message):
            if self.typeof("location")(message):
                return (pow(abs(message.location_x-latitude), 2) +
                        pow(abs(message.location_y-longitude), 2)) < pow(range, 2)
            return False
        return decorated_func


def all(m): return True


def and_(*funcs):
    def __call(*args, **kwargs):
        return reduce(lambda func_a, func_b: (func_a if type(func_a) == bool else
                                              func_a(*args, **kwargs)) and func_b(*args, **kwargs), funcs)
    return __call


def or_(*funcs):
    def __call(*args, **kwargs):
        return reduce(lambda func_a, func_b: (func_a if type(func_a) == bool else
                                              func_a(*args, **kwargs)) or func_b(*args, **kwargs), funcs)
    return __call


event = Event()
message = Message()
