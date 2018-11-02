__name__ = "location"

def test(msg):
    return msg.msg_type == "location"

def respond(msg):
    import time, requests
    url = "http://api.map.baidu.com/timezone/v1"
    params = {
        "location":"%f,%f".format(msg.location_x,msg.location_y),
        "coord_type":"wgs84",
        "timestamp": int(time.time()),
        "ak":"D83b70d1f9d39d9998d6cc544b27a55b"
    }

    r = requests.get(url,params)

    return "text", {"Content": r.text}