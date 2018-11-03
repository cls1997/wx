__name__ = "location"


def test(msg):
    return msg.msg_type == "location"


# def respond(msg):
#     import time
#     import requests

#     url = "http://api.map.baidu.com/timezone/v1?location={},{}".format(
#         msg.location_x, msg.location_y)
#     # make comma dont encode 
#     params = {
#         "coord_type": "wgs84ll",
#         "timestamp": int(time.time()),
#         "ak": "ivTL8OfP0G8gOeUYaMSP9SHfuXcxKfDX"
#     }

#     r = requests.get(url, params)

#     return "text", {"Content": r.text}
def respond(msg):
    from app.api.baidueagle import entity_create, entity_list, track_addpoint

    wechat_user = msg.FromUserName
    if entity_list(wechat_user)['status'] == 3003:
        entity_create(wechat_user)

    track_addpoint(wechat_user, msg.latitude, msg.longitude, msg.create_time)