import json
import time

import requests
from flask import Blueprint, current_app, render_template, request

js_sdk = Blueprint("js_sdk", __name__, template_folder='templates', static_folder='static')


class Sign:
    def __init__(self):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': current_app.wechat.client.js_sdk.get_ticket(),
            'timestamp': int(time.time()),
            'url': request.url,
        }

    @staticmethod
    def __create_nonce_str():
        import string
        import random
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def sign(self):
        import hashlib
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key])
                           for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(
            string.encode('utf-8')).hexdigest()
        return self.ret


def query(key: str) -> dict:
    """
    ICiba api
    :param key:
    :return: dict
    """
    url = 'http://dict-co.iciba.com/api/dictionary.php'
    params = {
        'w': key,
        'key': current_app.config.get("CIBA_KEY"),
        'type': 'json'
    }
    r = requests.get(url, params)

    try:
        return json.loads(r.content)
    except Exception as e:
        current_app.logger.exception(e)
        return None


@js_sdk.route("")
def index():
    app_id = current_app.config.get('WECHAT_APPID')
    sign = Sign().sign()

    key = request.args.get('key', default='go', type=str)
    result = None
    try:
        result = query(key)
    except Exception:
        pass

    return render_template("index.html",
                           appId=app_id,
                           sign=sign,
                           time=int(time.time()),
                           result=result,
                           key=key
                           )


@js_sdk.route('/sample')
def sample():
    app_id = current_app.config.get('WECHAT_APPID')
    sign = Sign().sign()
    return render_template("sample.html",
                           appId=app_id,
                           timestamp=sign['timestamp'],
                           nonceStr=sign['nonceStr'],
                           signature=sign['signature']
                           )
