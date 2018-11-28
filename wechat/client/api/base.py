class BaseAPICollection:
    def __init__(self, client=None):
        self.client = client

    def _get(self, **kwargs):
        self.client.get(**kwargs)

    def _post(self, **kwargs):
        self.client.post(**kwargs)

    @property
    def access_token(self):
        return self.client.access_token

    @property
    def appid(self):
        return self.client.app_id
