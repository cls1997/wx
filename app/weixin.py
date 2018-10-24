from flask import Blueprint, current_app, request, jsonify
import hashlib

weixin = Blueprint('weixin', __name__, url_prefix='/wechat')


@weixin.route("/", methods=['POST'])
def handle_post():
    pass


@weixin.route("/", methods=['GET'])
def handle_get():
    params = request.args
    signature = params.get("signature", "")
    timestamp = params.get("timestamp", "")
    nonce = params.get("nonce", "")
    echostr = params.get("echostr", "")

    if (current_app.wechat.check_signature(signature, timestamp, nonce)):
        return echostr

    if(current_app.debug):
        return "DEBUG"

class WechatMessageHandler:
    def __init__(self, token, app_secret, app):
        self.__token = token
        self.__app_secret = app_secret
        self.__app = app

    def check_signature(self, signature, timestamp, nonce):
        if not signature or not timestamp or not nonce:
            return False

        tmp_list = [self.__token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)

        if signature != hashlib.sha1(tmp_str.encode('utf-8')).hexdigest():
            return False
        return True

    def send_message(self):
        pass

    def handle_message(self):
        pass

    def handle_event(self):
        pass