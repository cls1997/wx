from flask import Flask
from .base import MyResponse
from .weixin import weixin


def create_app():
    app = Flask(__name__)
    app.config["TOKEN"] = "wechat"
    app.response_class = MyResponse
    app.register_blueprint(weixin)
    # app.("TOKEN", "wechat")("APPSECRET", "2043c4d45968c088048d9782cb69a988");
    return app
