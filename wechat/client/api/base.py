class BaseAPICollection:
    def __init__(self, client=None):
        self.client = client

    def _get(self, **kwargs):
        return self.client.get(**kwargs)

    def _post(self, **kwargs):
        return self.client.post(**kwargs)

    @property
    def access_token(self):
        return self.client.access_token

    @property
    def app_id(self):
        return self.client.app_id
