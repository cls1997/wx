__name__ = 'baidueagle'

import json
import os

import requests

ak = os.environ.get("LBS_AK")
eagle_service_id = os.environ.get("EAGLE_SERVICE_ID")


def entity_create(wechat_user):
    url = "http://yingyan.baidu.com/api/v3/entity/add"
    datas = {
        "ak": ak,
        "service_id": eagle_service_id,
        "entity_name": wechat_user
    }

    r = requests.post(url, data=datas)
    print(json.dumps(datas))
    return r.json()


def entity_list(wechat_user):
    url = "http://yingyan.baidu.com/api/v3/entity/list"
    datas = {
        "ak": ak,
        "service_id": eagle_service_id,
        "filter": "entity_names:{}".format(wechat_user)
    }

    r = requests.get(url, "&".join('{}={}'.format(k, v)
                                   for k, v in datas.items()))
    return r.json()


def track_addpoint(wechat_user, latitude, longitude, loc_time):
    url = 'http://yingyan.baidu.com/api/v3/track/addpoint'
    datas = {
        "ak": ak,
        "service_id": eagle_service_id,
        "entity_name": wechat_user,
        "latitude": latitude,
        "longitude": longitude,
        "loc_time": loc_time,
        "coord_type_input": "wgs84"
    }

    r = requests.post(url, data=datas)

    return r.json()
