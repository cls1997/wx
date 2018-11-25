import unittest

from app.wechat.messages import parse_wechat_message
from messages import messages


class MessageTest(unittest.TestCase):
    def setUp(self):
        self.messages = {k: parse_wechat_message(v)
                         for k, v in messages.items()}

    def test_attrs(self):
        message = self.messages["text1"]
        attrs = ['from_user_name', 'to_user_name', 'create_time', 'msg_type', 'msg_id', 'content',
                 'reply_text', 'reply_image', 'reply_voice', 'reply_video']
        for attr in attrs:
            self.assertTrue(hasattr(message, attr))
