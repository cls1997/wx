from . import WechatMessage

from .fields import StringField, IntegerField, FloatField
event_mapping = {}

def register_event(name):
    def register(cls):
        event_mapping[name] = cls
        return cls
    return register


class BaseEvent(WechatMessage):
    to_user_name = StringField("ToUserName")
    from_user_name = StringField("FromUserName")
    create_time = IntegerField("CreateTime")
    msg_type = StringField("MsgType")
    event = StringField("Event")


@register_event("subscribe")
class SubscribeEvent(BaseEvent):
    pass


@register_event("unsubscribe")
class UnsubscribeEvent(BaseEvent):
    pass


@register_event("click")
class ClickEvent(BaseEvent):
    event_key = StringField("EventKey")


@register_event("LOCATION")
class LocationEvent(BaseEvent):
    latitude = FloatField("Latitude")
    longitude = FloatField("Longitude")
    precision = FloatField("Precision")