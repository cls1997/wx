from wechat.client.api import (MediaAPI, JsSdkAPI)
from wechat.client.api.menu import MenuAPI
from wechat.client.base import BaseAPIClient

__all__ = ['WechatAPIClient']


class WechatAPIClient(BaseAPIClient):
    media = MediaAPI()
    js_sdk = JsSdkAPI()
    menu = MenuAPI()

    API_URL_PREFIX = 'https://api.weixin.qq.com/cgi-bin'

    @property
    def access_token(self):
        return self._access_token()

    @property
    def js_api_ticket(self):
        ticket = self.storage.get('js_sdk_ticket')
        if ticket is None:
            ticket = self.js_sdk.get_ticket()
            self.storage.set('js_sdk_ticket', ticket, 7200 - 60)
        return ticket
