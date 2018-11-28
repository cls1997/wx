from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

from wechat import Wechat

__all__ = ['wechat', 'redis', 'db']

wechat = Wechat()
db = SQLAlchemy()
redis = FlaskRedis()
