

class BaseHandler:
    def test(self, msg):
        raise NotImplementedError()

    def respond(self, msg):
        raise NotImplementedError()


__all__ = ['repeater','location']
