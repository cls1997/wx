import hashlib
import logging
import time

from app.wechatmessage import build_wechat_reply,parse_wechat_message
import app.handlers


class WechatAPI:
    logger = logging.getLogger("WechatAPI")
    _handlers = []
    _handler_loaded = False

    def __init__(self, token, app_secret, app):
        self.__token = token
        self.__app_secret = app_secret
        self.__app = app
        self.load_handlers()

    @classmethod
    def register_handler(cls, handler):
        if not hasattr(handler, 'test'):
            logging.error('Handler %s has no method named test, ignore it')
            return False
        if not hasattr(handler, 'respond'):
            logging.error('Handler %s has no method named respond, ignore it')
            return False
        cls._handlers.append(handler)
        cls.logger.info("%s has registered.", handler)
        return True

    @classmethod
    def load_handlers(cls):
        if not cls._handler_loaded:
            for name in app.handlers.__all__:
                try:
                    __import__('app.handlers.%s' % name)
                    cls.register_handler(getattr(app.handlers, name))
                except Exception as e:
                    logging.warning('Fail to load handler %s\n %s %s',
                                    name, e, 'handlers.%s' % name)

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
            msg = parse_wechat_message(msg)
            self.logger.info(
                "Message parsed.Type {}, Id {}".format(type(msg), msg.msg_id))
        except RuntimeError:
            self.logger.exception("Processing: {}".format(msg))
            return ""
        finally:
            self.logger.debug("Message parsing over.")

        # TODO Message Handlers
        # Input a BaseMessage return a BaseReply
        response = self.make_response(msg)

        self.logger.debug(response)
        return response

    def make_response(self, msg):
        # TODO stupid code
        start = time.time()
        response = {}
        msg_type = "text"
        for handler in self._handlers:
            if handler.test(msg):
                msg_type, response = handler.respond(msg)

        response = build_wechat_reply(msg, msg_type, response)

        self.logger.info("It spent %dms to make this response.",
                         int((time.time()-start)*1000))
        return response or ""
