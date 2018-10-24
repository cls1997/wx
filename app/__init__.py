from flask import Flask
from .base import MyResponse
from .weixin import weixin
from .webhooks import webhook
import os 


def create_app():
    from logging.config import dictConfig

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })



    app = Flask(__name__)
    app.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
    app.config['REPO_PATH'] = os.environ.get('REPO_PATH')

    app.response_class = MyResponse

    from .weixin import WechatMessageHandler
    app.wechat = WechatMessageHandler(
        os.environ.get("WECHAT_TOKEN"),
        os.environ.get("WECHAT_APP_SECRET"),
        app
        )


    app.register_blueprint(weixin)
    app.register_blueprint(webhook)
    return app
