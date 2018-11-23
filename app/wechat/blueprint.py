import hashlib
import hmac
import time

from flask import Blueprint, Response
from flask import current_app, jsonify, request, g

wechat = Blueprint('wechat', __name__, url_prefix='/wechat')


@wechat.before_request
def before_request():
    g.start_time = time.time()


@wechat.teardown_request
def teardown_request(exception=None):
    diff = time.time() - g.start_time
    current_app.logger.info(
        "It spent %dms to handle this request.", int(1000*diff))


@wechat.route("", methods=['POST'])
def handle_post():
    post_data = request.data.decode(encoding="utf-8", errors="strict")
    return Response(current_app.wechat.handle_message(post_data),
                    mimetype='application/xml')


@wechat.route("", methods=['GET'])
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
    else:
        return ""
