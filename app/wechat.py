import hashlib
import logging

from enum import Enum, auto
from app.wechatmessage import build_wechat_message, parse_wechat_message, ReplyFactory


class WechatAPI:
    def __init__(self, token, app_secret, app):
        self.__token = token
        self.__app_secret = app_secret
        self.__app = app
        self.__handlers = {}
        self.logger = logging.getLogger("WechatAPI")

    def register_handler(self, handler):
        self.logger.info("%s has registered.")

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

        """
        try:
            self.logger.info("Message before parsing: {}" .format(msg))
            msg_id, msg = parse_wechat_message(msg)
            self.logger.info(
                "Message parsed.Type {}, Id {}".format(type(msg), msg_id))
        except RuntimeError:
            self.logger.exception("Processing: {}".format(msg))
            return ""
        finally:
            self.logger.debug("Message parsing over.")

        #TODO Message Handlers
        response = ReplyFactory(msg)
        response = response.render(**{"content": "QWEQWE"})

        self.logger.debug(response)
        return build_wechat_message(response)