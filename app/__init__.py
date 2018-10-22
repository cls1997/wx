from flask import Flask
from .base import MyResponse
from .weixin import weixin
import os 


def create_app():
    app = Flask(__name__)
    app.config["TOKEN"] = os.environ.get("WECHAT_TOKEN")
    app.config["APP_SECRET"] = os.environ.get("WECHAT_APP_SECRET")
    app.response_class = MyResponse
    app.register_blueprint(weixin)
    return app
