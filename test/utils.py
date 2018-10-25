xmlstring = """<xml>
    <ToUserName><![CDATA[0000]]></ToUserName>
    <FromUserName><![CDATA[000]]></FromUserName>
    <CreateTime>1540382492</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[message]]></Content>
    <MsgId>1234567890abcdef</MsgId>
</xml>"""

from app.utils import parse_wechat_message, build_wechat_message

msg = parse_wechat_message(xmlstring)

print(msg.tag)

d = {}

for child in msg:
    if child == "ToUserName":
        print("OK")
    d[child.tag] = child.text
    print(" ", msg.find(child.tag).text)
    print("\n")

build_wechat_message(msg)

