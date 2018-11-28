import unittest

from test.messages import messages
from wechat.messages import parse_wechat_message


class MessageTest(unittest.TestCase):
    def setUp(self):
        self.messages = {k: parse_wechat_message(v)
                         for k, v in messages.items()}

    def test_attrs(self):
        message = self.messages["text1"]
        attrs = ['from_user_name', 'to_user_name', 'create_time', 'msg_type', 'msg_id', 'content',
                 'FromUserName', 'ToUserName', 'CreateTime', 'MsgType', 'MsgId', 'Content',
                 'reply_text', 'reply_image', 'reply_voice', 'reply_video']
        for attr in attrs:
            self.assertTrue(hasattr(message, attr))

        self.assertTrue(message.from_user_name == message.FromUserName)
        self.assertTrue(isinstance(message.from_user_name, str))
        self.assertTrue(isinstance(message.msg_id, int))
