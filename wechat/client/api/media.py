from wechat.client.api.base import BaseAPICollection


class MediaAPI(BaseAPICollection):
    def upload(self, media_type, media_file):
        """
        :param media_type: image/voice/video/thumb
        :param media_file: 
        """
        return self.post(
            endpoint='/media/upload',
            params={
                'type': media_type,
                'access_token': self.access_token
            },
            files={
                'media': media_file
            },
            result_processor=lambda r: r['media_id']
        )
