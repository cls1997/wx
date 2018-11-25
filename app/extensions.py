from wechat import Wechat
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

__all__ = ['wechat', 'redis', 'db']

wechat = Wechat()
db = SQLAlchemy()
redis = FlaskRedis()
