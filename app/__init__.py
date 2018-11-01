import logging
import os

from flask import Flask
from flask.logging import default_handler


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
            'level': 'DEBUG',
            'handlers': ['wsgi']
        },
        "flask.app": {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        },
        "WechatAPI": {
            'level': 'DEBUG',
            'handlers': ['wsgi']
        }
    })
    app = Flask(__name__)
    
    # for logger in (
    #     app.logger,
    #     logging.getLogger("WechatAPI"),
    # ):
    #     logger.addHandler(default_handler)

    app.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
    app.config['REPO_PATH'] = os.environ.get('REPO_PATH')

    from .wechat import WechatAPI
    app.wechat = WechatAPI(
        os.environ.get("WECHAT_TOKEN"),
        os.environ.get("WECHAT_APP_SECRET"),
        app
    )

    from .controller import wechat, github
    app.register_blueprint(wechat)
    app.register_blueprint(github)
    return app
