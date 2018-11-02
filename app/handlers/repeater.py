__name__ = 'repeater'


def test(self, msg):
    return msg.msg_type == "text"

def respond(self, msg):
    return {"Content": msg.content}