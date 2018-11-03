__name__ = 'location_event'
"""
<xml>
    <ToUserName>< ![CDATA[toUser] ]></ToUserName>
    <FromUserName>< ![CDATA[fromUser] ]></FromUserName>
    <CreateTime>123456789</CreateTime>
    <MsgType>< ![CDATA[event] ]></MsgType>
    <Event>< ![CDATA[LOCATION] ]></Event>
    <Latitude>23.137466</Latitude>
    <Longitude>113.352425</Longitude>
    <Precision>119.385040</Precision>
</xml>
"""

from app.api.baidueagle import entity_create, entity_list, track_addpoint


def test(msg):
    return (msg.msg_type == "event"
            and msg.event == "LOCATION")


def respond(msg):
    wechat_user = msg.FromUserName
    if entity_list(wechat_user)['status'] == 3003:
        entity_create(wechat_user)

    track_addpoint(wechat_user, msg.location_x, msg.location_y, msg.create_time)