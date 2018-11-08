import os
import sys
import logging

from flask import Flask


def create_app():
    app = Flask(__name__)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    loggers = ['root', 'flask.app']
    level = logging.INFO if app.debug else logging.DEBUG

    for logger in loggers:
        logger = logging.getLogger(logger)
        logger.setLevel(level)
        logger.addHandler(console_handler)
        if not app.debug:
            logger.addHandler(
                logging.handlers.WatchedFileHandler("{}/wechat.log".format(sys.path[0]))
            )
            


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
