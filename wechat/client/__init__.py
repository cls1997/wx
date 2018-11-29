from wechat.client.api import (MediaAPI)
from wechat.client.base import BaseAPIClient

__all__ = ['WechatAPIClient']


class WechatAPIClient(BaseAPIClient):
    media = MediaAPI()

    API_URL_PREFIX = 'https://api.weixin.qq.com/cgi-bin'

    @property
    def access_token(self):
        return self._access_token()
