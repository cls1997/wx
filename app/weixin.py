from flask import Blueprint, current_app, request, jsonify
import hashlib

weixin = Blueprint('weixin', __name__, url_prefix='/wechat')


@weixin.route("/", methods=['POST'])
def handle_post():
    pass


@weixin.route("/", methods=['GET'])
def handle_get():
    params = request.args
    signature = params.get("signature", None)
    timestamp = params.get("timestamp", None)
    nonce = params.get("nonce", None)
    token = current_app.config.get("TOKEN")

    if (check_signature(signature, timestamp, nonce, token)):
        return params.get("echostr")

    if(current_app.debug):
        return token


def check_signature(signature, timestamp, nonce, token):
    if not signature or not timestamp or not nonce:
        return False

    tmp_list = [token, timestamp, nonce]
    tmp_list.sort()
    tmp_str = ''.join(tmp_list)

    if signature != hashlib.sha1(tmp_str.encode('utf-8')).hexdigest():
        return False
    return True
