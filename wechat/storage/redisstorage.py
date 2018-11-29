from wechat.storage import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, redis, prefix='wechat'):
        for method_name in ('get', 'set', 'delete'):
            assert hasattr(redis, method_name)
        self.redis = redis
        self.prefix = prefix

    def key_name(self, key):
        return '{0}:{1}'.format(self.prefix, key)

    def get(self, key, default=None):
        key = self.key_name(key)
        value = self.redis.get(key)
        if value is None:
            return default
        return value.decode('utf-8')

    def set(self, key, value, ttl=None):
        if value is None:
            return
        key = self.key_name(key)
        self.redis.set(key, value, ex=ttl)

    def delete(self, key):
        key = self.key_name(key)
        self.redis.delete(key)
