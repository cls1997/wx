import unittest

import app.wechat.filters as filters
from app.wechat.messages import parse_wechat_message
from messages import messages


class MessageFilterTest(unittest.TestCase):
    def test_all_filter(self):
        self.assertTrue(filters.all(parse_wechat_message(messages['text1'])))

    def do_message_filter_test(self, filter, result):
        messages_ = {k: parse_wechat_message(v)
                     for k, v in messages.items()}
        rv = True
        self.assertTrue(len(messages_) == len(result))
        filter_ = filter
        l = []
        for v in messages_.values():
            l.append(filter_(v))

        while l and rv:
            rv = rv and (l.pop() == result.pop())

        return rv

    def test_message_filter(self):
        self.assertTrue(self.do_message_filter_test(
            filters.message.text(),
            [True, True, False,  False, False, False]
        ))
        self.assertTrue(self.do_message_filter_test(
            filters.message.image,
            [False, False, True, False, False, False]
        ))
        self.assertTrue(self.do_message_filter_test(
            filters.message.voice,
            [False, False, False, True, False, False]
        ))
        self.assertTrue(self.do_message_filter_test(
            filters.message.video,
            [False, False, False,  False, True, False]
        ))
        self.assertTrue(self.do_message_filter_test(
            filters.message.typeof('location'),
            [False, False, False,  False, False, True]
        ))
        self.assertTrue(self.do_message_filter_test(
            filters.message.startswith("msg"),
            [True, False, False,  False, False, False]
        ))
        self.assertTrue(self.do_message_filter_test(
            filters.message.contains("ess"),
            [False, True, False,  False, False, False]
        ))
    
    def test_location_filter(self):
        msg = parse_wechat_message(messages.get('location'))
        self.assertTrue(
            filters.message.location(msg.location_x,msg.location_y,1)(msg)
        )
        self.assertFalse(
            filters.message.location(msg.location_x+2,msg.location_y,1)(msg)
        )

    def test_common_filter(self):
        def t(m): return True

        def f(m): return False
        m = parse_wechat_message(messages["text1"])

        self.assertTrue(filters.all(m))

        self.assertTrue(filters.or_(t, t)(m) == True)
        self.assertTrue(filters.or_(f, t)(m) == True)
        self.assertTrue(filters.or_(t, f)(m) == True)
        self.assertFalse(filters.or_(f, f)(m) == True)
        self.assertTrue(filters.or_(t, t, t)(m) == True)
        self.assertTrue(filters.or_(t, t, f)(m) == True)
        self.assertTrue(filters.or_(t, f, t)(m) == True)
        self.assertTrue(filters.or_(t, f, f)(m) == True)
        self.assertTrue(filters.or_(f, t, t)(m) == True)
        self.assertTrue(filters.or_(f, t, f)(m) == True)
        self.assertTrue(filters.or_(f, f, t)(m) == True)
        self.assertFalse(filters.or_(f, f, f)(m) == True)

        self.assertTrue(filters.and_(t, t)(m) == True)
        self.assertFalse(filters.and_(t, f)(m) == True)
        self.assertFalse(filters.and_(f, t)(m) == True)
        self.assertFalse(filters.and_(f, f)(m) == True)
        self.assertTrue(filters.and_(t, t, t)(m) == True)
        self.assertFalse(filters.and_(t, t, f)(m) == True)
        self.assertFalse(filters.and_(t, f, t)(m) == True)
        self.assertFalse(filters.and_(t, f, f)(m) == True)
        self.assertFalse(filters.and_(f, t, t)(m) == True)
        self.assertFalse(filters.and_(f, t, f)(m) == True)
        self.assertFalse(filters.and_(f, f, t)(m) == True)
        self.assertFalse(filters.and_(f, f, f)(m) == True)
