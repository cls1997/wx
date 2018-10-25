import sys

from app.wechatmessage import WechatMessage, NormalParam, CdataParam,WechatTextMessage
from app.utils import etree





a = {"ToUserName":"123","FromUserName":"312","Content":"123","CreateTime":123}

msg = WechatTextMessage(**a)
root = msg.serialize()
etree.ElementTree(root).write(sys.stdout.buffer)

#
# print(type(a))
# print(isinstance(a, dict))
