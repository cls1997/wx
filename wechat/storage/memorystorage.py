import time

from . import BaseStorage


class MemoryStorage(BaseStorage):
    def __init__(self):
        self._storage = {}
        self._expire_at = {}

    def _expire(self, key):
        try:
            return self._expire_at[key] < int(time.time())
        except KeyError:
            return True

    def get(self, key):
        if self._expire(key):
            return None
        return self._storage.get(key)

    def set(self, key, value, ttl=None):
        if value is None:
            return
        self._storage[key] = value
        if ttl:
            self._expire_at[key] = ttl + int(time.time())

    def delete(self, key):
        self._expire_at.pop(key, None)
        self._storage.pop(key, None)
