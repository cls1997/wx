# coding: utf8
from wechat.client.api.base import BaseAPICollection


class JsSdkAPI(BaseAPICollection):
    def get_ticket(self):
        return self.get(
            endpoint="/ticket/getticket",
            params={
                'type': 'jsapi',
                'access_token': self.access_token
            },
            result_processor=lambda result: result['ticket']
        )
