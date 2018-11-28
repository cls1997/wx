class BaseStorage:
    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, ttl):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
