import hashlib
import logging
import time

import wechat.filters as filters
from wechat.blueprint import wechat as wechat_blueprint
from wechat.client import WechatAPIClient
from wechat.messages import parse_wechat_message
from wechat.storage.redisstorage import RedisStorage

__all__ = ["Wechat", 'filters']


def _callable(func): return hasattr(func, "__call__")


class Wechat:
    logger = logging.getLogger("WechatAPI")

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    # noinspection PyAttributeOutsideInit
    def init_app(self, app):
        storage = None
        if 'redis' in app.extensions:
            storage = RedisStorage(app.extensions['redis'])
        self.app = app
        self.__token = app.config.get('WECHAT_TOKEN')
        self.__app_id = app.config.get('WECHAT_APPID')
        self.__app_secret = app.config.get('WECHAT_APP_SECRET')
        self.client = WechatAPIClient(self.__app_id, self.__app_secret, storage)
        app.register_blueprint(wechat_blueprint)
        app.wechat = self

    _handlers = []

    def register_filter(self, filters_):
        """
        Handler Register Function
        A handler takes a BaseMessage object and returns a BaseReply object

        @wechat.handler(filter)
        def handler(message):
            return message.reply_text("A Reply")
        """

        def decorator(func):
            _filters = filters_
            if not _filters:
                _filters = filters.all
            elif isinstance(_filters, list):
                if len(list(filter(lambda f: not _callable(f), _filters))):
                    raise TypeError("filters must be callable")
                _filters = filters.and_(_filters)
            elif not _callable(_filters):
                raise TypeError("filters must be callable")

            for tuple_ in self._handlers:
                if tuple_[0] == _filters:
                    del self._handlers[tuple_]
                    break

            if _filters == filters.all:
                self._handlers.append((_filters, func))
            else:
                # Last Defined First Called
                self._handlers.insert(0, (_filters, func))

            return func

        return decorator

    def do_filter(self, message):
        def get_handler(msg):
            for filter_, handler in self._handlers:
                if filter_(msg):
                    return handler
            return None

        handler = get_handler(message)
        if handler is not None:
            return handler(message)

    def check_signature(self, signature, timestamp, nonce):
        if not signature or not timestamp or not nonce:
            return False

        tmp_list = [self.__token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)

        if signature != hashlib.sha1(tmp_str.encode('utf-8')).hexdigest():
            return False
        return True

    def handle_message(self, msg):
        """
        TODO: We need INTERCEPTOR!!!
        """
        self.logger.info("Message before parsing: {}".format(msg))
        start = time.time()
        msg = parse_wechat_message(msg)
        self.logger.info(
            "Message parsed.Type {}, Id {}".format(type(msg), msg.msg_id))
        self.logger.debug("Message parsing over.")

        # Input a BaseMessage return a BaseReply
        reply = self.do_filter(msg)

        self.logger.debug(reply)
        self.logger.info("It spent %dms to make this response.",
                         int((time.time() - start) * 1000))
        return reply
