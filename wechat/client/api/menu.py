# coding: utf8
from wechat.client.api.base import BaseAPICollection


class MenuAPI(BaseAPICollection):
    def create(self, menu):
        return self.post(
            endpoint='/menu/create',
            params={
                'access_token': self.access_token,
            },
            data=menu
        )

    def delete(self):
        return self.post(
            endpoint='/menu/delete',
            params={
                'access_token': self.access_token
            }
        )
