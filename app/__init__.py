from flask import Flask
from .base import MyResponse
from .weixin import weixin
from .webhooks import webhook
import os 


def create_app():
    app = Flask(__name__)
    app.config["TOKEN"] = os.environ.get("WECHAT_TOKEN")
    app.config["APP_SECRET"] = os.environ.get("WECHAT_APP_SECRET")
    app.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
    app.config['REPO_PATH'] = os.environ.get('REPO_PATH')

    app.response_class = MyResponse

    app.register_blueprint(weixin)
    app.register_blueprint(webhook)
    return app
