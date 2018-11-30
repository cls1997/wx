import hashlib
import time
import random
import time
import string
import requests
import json

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


def get_jsapi_ticket(app):
    access_token = app.wechat.client.access_token

    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'.format(
        access_token)

    r = requests.get(url)
    try:
        r = json.loads(r.content)
    except Exception as e:
        app.logger.exception(e)
    return r['ticket']


@jssdk.route("/")
def index():
    sign = Sign(
        get_jsapi_ticket(current_app),
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
