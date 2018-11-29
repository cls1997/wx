from flask import current_app

__name__ = "baidulbs"

import requests

ak = current_app.config.get("LBS_AK")


def get_image(latitude, longitude):
    longitude = longitude
    latitude = latitude

    url = "http://api.map.baidu.com/staticimage/v2"
    datas = {
        "ak": ak,
        "center": "{},{}".format(longitude, latitude),
        "width": 300,
        "height": 200,
        "zoom": 11
    }

    r = requests.get(url, "&".join('{}={}'.format(k, v)
                                   for k, v in datas.items()))
    print(r.url)
    return r.content
