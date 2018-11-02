import time
import requests
import urllib

url = "http://api.map.baidu.com/timezone/v1?location={},{}".format(123.3,12.3)
params = {
    "coord_type": "wgs84",
    "timestamp": int(time.time()),
    "ak": "ivTL8OfP0G8gOeUYaMSP9SHfuXcxKfDX"
}

# encodedStr = urllib.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

r = requests.get(url, params)
print(r.url)
