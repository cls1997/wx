import hashlib

from .utils import build_wechat_message, parse_wechat_message

class WechatAPI:
    def __init__(self, token, app_secret, app):
        self.__token = token
        self.__app_secret = app_secret
        self.__app = app
        self.__handlers = {}

    def register_handler(self, handler):
        pass

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
        root = parse_wechat_message(msg)
        return build_wechat_message(root).decode(encoding="utf-8", errors="strict")

    def send_message(self, msg):
        pass
