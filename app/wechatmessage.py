class Param:
    def __init__(self, name, is_cdata):
        self.name = name
        self.is_cdata = is_cdata

    def __str__(self):
        return "<%s:%s>" % (self.name, self.is_cdata)


class NormalParam(Param):
    def __init__(self, name):
        super(NormalParam, self).__init__(name, False)


class CdataParam(Param):
    def __init__(self, name):
        super(CdataParam, self).__init__(name, True)


class WechatMessageMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "WechatMessage":
            return type.__new__(cls, name, bases, attrs)
        data = dict()
        for k, v in attrs.items():
            if isinstance(v, Param):
                print('Found Param: %s==>%s' % (k, v))
                data[k] = v
        for k in data.keys():
            attrs.pop(k)
        attrs["__data__"] = data
        return type.__new__(cls, name, bases, attrs)


class WechatMessage(dict, metaclass=WechatMessageMetaclass):
    def __init__(self, **kw):
        print("kw ", kw)
        super(WechatMessage, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'%s' object has no attribute '%s'" % (self.__class__, key))

    def __setattr__(self, key, value):
        self[key] = value

    def serialize(self):
        from app.utils import cdata, etree

        def foo(parent, kvs):
            for k, v in kvs.items():
                elem = etree.Element(v.name)
                if isinstance(v, Param):
                    value = getattr(self, v.name, None)
                else:
                    raise AttributeError(
                        "%s is not a valid type" % type(v))

                if isinstance(value, dict):
                    foo(elem, value)
                elif isinstance(v, CdataParam):
                    elem.append(cdata(value))
                elif isinstance(value, int):
                    elem.text = "%d" % value
                else:
                    elem.text = value

                print(elem.tag)
                parent.append(elem)

        root = etree.Element("xml")
        foo(root, self.__data__)
        return root


class WechatTextMessage(WechatMessage):
    """
    参数	是否必须	描述
    ToUserName	是	接收方帐号（收到的OpenID）
    FromUserName	是	开发者微信号
    CreateTime	是	消息创建时间 （整型）
    MsgType	是	text
    """
    to_user_name = CdataParam("ToUserName")
    from_user_name = CdataParam("FromUserName")
    create_time = NormalParam("CreateTime")
    msg_type = CdataParam("MsgType")
    content = CdataParam("Content")

    def __init__(self, **kw):
        self["MsgType"] = "text"
        super().__init__(**kw)


"""
参数	        是否必须	描述
ToUserName	    是	       收方帐号（收到的OpenID）
FromUserName	是	        开发者微信号
CreateTime	    是	        消息创建时间 （整型）
MsgType	        是	        text
Content	        是	        回复的消息内容（换行：在content中能够换行，微信客户端就支持换行显示）

发：
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[你好]]></Content>
</xml>

收：
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>1348831860</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[this is a test]]></Content>
    <MsgId>1234567890123456</MsgId>
</xml>
"""

"""
回复图片消息
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <Image>
        <MediaId><![CDATA[media_id]]></MediaId>
    </Image>
</xml>
参数	是否必须	说明
ToUserName	是	接收方帐号（收到的OpenID）
FromUserName	是	开发者微信号
CreateTime	是	消息创建时间 （整型）
MsgType	是	image
MediaId	是	通过素材管理中的接口上传多媒体文件，得到的id。

回复语音消息
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[voice]]></MsgType>
    <Voice>
        <MediaId><![CDATA[media_id]]></MediaId>
    </Voice>
</xml>
参数	是否必须	说明
ToUserName	是	接收方帐号（收到的OpenID）
FromUserName	是	开发者微信号
CreateTime	是	消息创建时间戳 （整型）
MsgType	是	语音，voice
MediaId	是	通过素材管理中的接口上传多媒体文件，得到的id

回复视频消息
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[video]]></MsgType>
    <Video><MediaId><![CDATA[media_id]]></MediaId>
        <Title><![CDATA[title]]></Title>
        <Description><![CDATA[description]]></Description>
    </Video>
</xml>
参数	是否必须	说明
ToUserName	是	接收方帐号（收到的OpenID）
FromUserName	是	开发者微信号
CreateTime	是	消息创建时间 （整型）
MsgType	是	video
MediaId	是	通过素材管理中的接口上传多媒体文件，得到的id
Title	否	视频消息的标题
Description	否	视频消息的描述

回复音乐消息
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
        <Title><![CDATA[TITLE]]></Title>
        <Description><![CDATA[DESCRIPTION]]></Description>
        <MusicUrl><![CDATA[MUSIC_Url]]></MusicUrl>
        <HQMusicUrl><![CDATA[HQ_MUSIC_Url]]></HQMusicUrl>
        <ThumbMediaId><![CDATA[media_id]]></ThumbMediaId>
    </Music>
</xml>
参数	是否必须	说明
ToUserName	是	接收方帐号（收到的OpenID）
FromUserName	是	开发者微信号
CreateTime	是	消息创建时间 （整型）
MsgType	是	music
Title	否	音乐标题
Description	否	音乐描述
MusicURL	否	音乐链接
HQMusicUrl	否	高质量音乐链接，WIFI环境优先使用该链接播放音乐
ThumbMediaId	是	缩略图的媒体id，通过素材管理中的接口上传多媒体文件，得到的id

回复图文消息
<xml>
    <ToUserName><![CDATA[toUser]]></ToUserName>
    <FromUserName><![CDATA[fromUser]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>1</ArticleCount>
    <Articles>
        <item>
            <Title><![CDATA[title1]]></Title>
            <Description><![CDATA[description1]]></Description>
            <PicUrl><![CDATA[picurl]]></PicUrl>
            <Url><![CDATA[url]]></Url>
        </item>
    </Articles>
</xml>
"""
