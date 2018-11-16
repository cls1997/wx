__name__ = "wechat"

import os
import requests
import json
import sys

APPID = os.environ.get("WECHAT_APPID")
APPSECRET = os.environ.get("WECHAT_APP_SECRET")


def _get_ak():
    url = "https://api.weixin.qq.com/cgi-bin/token"
    datas = {
        "grant_type": "client_credential",
        "appid": APPID,
        "secret": APPSECRET
    }

    r = requests.get(url, datas)
    return r.json


def get_ak():
    return "15_Zmp9IlXqCtP1K5I9gKRE8MQMbqP9M28Ej47NVnLHBKjR-_DAInULDtzk6fgXL_bswBgIuwJBwbA-eqs3k-s-UNJXCdGl2Lf1uCky2kecpq4kQJtdG7f12C5gstdwkQ4YoDH369pY8IQMTc0CHRYdAFAPZG"


def upload_img(img):
    url = "https://api.weixin.qq.com/cgi-bin/media/upload"
    datas = {
        "access_token": get_ak(),
        "type": "image"
    }
    files = {"media": ('a.png', img)}

    r = requests.post(url, data=datas, files=files)

    resp = r.json()
    return resp["media_id"]
