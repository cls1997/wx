import hashlib
import random
import string
import time

from flask import Blueprint, current_app, render_template, request

jssdk = Blueprint("jssdk", __name__, template_folder='templates')


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key])
                           for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(
            string.encode('utf-8')).hexdigest()
        return self.ret


@jssdk.route("/")
def index():
    sign = Sign(
        current_app.wechat.client.js_sdk.get_ticket(),
        request.base_url
    )

    app_id = current_app.config.get('WECHAT_APPID')
    sign = sign.sign()
    return render_template("index.html",
                           appId=app_id,
                           timestamp=sign['timestamp'],
                           nonceStr=sign['nonceStr'],
                           signature=sign['signature']
                           )
