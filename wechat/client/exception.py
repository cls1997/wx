# coding: utf8

class WechatAPIException(Exception):

    def __init__(self, errcode, errmsg, client, request, response) -> None:
        self.errcode = errcode
        self.errmsg = errmsg
        self.client = client
        self.request = request
        self.response = response

    def __str__(self):
        if self.errcode and self.errmsg:
            return "ErrCode {} : {} \n" \
                   "{} {}" \
                .format(self.errcode, self.errmsg, self.request, self.response)


class APILimitedException(WechatAPIException):
    pass
