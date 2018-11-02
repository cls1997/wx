__name__ = 'repeater'


def test(msg):
    return msg.msg_type == "text"

def respond(msg):
    return {"Content": msg.content}