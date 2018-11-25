import os
import sys
import logging
import logging.handlers

from flask import Flask

from app.extensions import wechat, db, redis


def create_app():
    app = Flask(__name__)

    formatter = logging.Formatter(
        '[%(asctime)s] {%(name)s} %(levelname)s in %(module)s:\n\t %(message)s'
    )
    level = logging.DEBUG
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    loggers = ['root', 'flask.app', 'WechatAPI']

    for logger in loggers:
        logger = logging.getLogger(logger)
        logger.setLevel(level)
        logger.addHandler(console_handler)
        if not app.debug:
            file_handler = logging.handlers.WatchedFileHandler(
                "{}/wechat.log".format(sys.path[0]))
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)

    app.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
    app.config['REPO_PATH'] = os.environ.get('REPO_PATH')

    app.config['WECHAT_TOKEN'] = os.environ.get('WECHAT_TOKEN')
    app.config['WECHAT_APPID'] = os.environ.get('WECHAT_APPID')
    app.config['WECHAT_APP_SECRET'] = os.environ.get('WECHAT_APP_SECRET')
    
    configure_extensions(app)

    from app.github import github
    app.register_blueprint(github)

    return app


def configure_extensions(app):
    db.init_app(app)
    wechat.init_app(app)
    redis.init_app(app)

import app.wechat_handlers