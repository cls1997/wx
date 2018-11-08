import os
import sys
import logging
import logging.handlers

from flask import Flask


def create_app():
    app = Flask(__name__)

    formatter = logging.Formatter(
        '[%(asctime)s] {%(name)s} %(levelname)s in %(module)s: %(message)s'
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

    app.config['GITHUB_SECRET']=os.environ.get('GITHUB_SECRET')
    app.config['REPO_PATH']=os.environ.get('REPO_PATH')

    from .wechat import WechatAPI
    app.wechat=WechatAPI(
        os.environ.get("WECHAT_TOKEN"),
        os.environ.get("WECHAT_APP_SECRET"),
        app
    )

    from .controller import wechat, github
    app.register_blueprint(wechat)
    app.register_blueprint(github)

    return app
