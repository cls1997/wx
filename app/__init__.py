import logging
import logging.handlers
import os
import sys

from flask import Flask


def create_app():
    application = Flask(__name__)

    formatter = logging.Formatter(
        '[%(asctime)s] {%(name)s} %(levelname)s in %(module)s:\n\t %(message)s'
    )
    level = logging.DEBUG  # TODO:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    loggers = ['root', 'flask.app', 'WechatAPI']

    for logger in loggers:
        logger = logging.getLogger(logger)
        logger.setLevel(level)
        logger.addHandler(console_handler)
        if not application.debug:
            file_handler = logging.handlers.WatchedFileHandler(
                "{}/wechat.log".format(sys.path[0]))
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)

    application.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
    application.config['REPO_PATH'] = os.environ.get('REPO_PATH')

    application.config['WECHAT_TOKEN'] = os.environ.get('WECHAT_TOKEN')
    application.config['WECHAT_APPID'] = os.environ.get('WECHAT_APPID')
    application.config['WECHAT_APP_SECRET'] = os.environ.get('WECHAT_APP_SECRET')

    application.logger.debug(application.config)

    configure_extensions(application)

    from app.github import github
    application.register_blueprint(github)

    import app.wechat_handlers

    return application


def configure_extensions(app):
    from app.extensions import wechat, db, redis
    # db.init_app(app)
    redis.init_app(app)
    # wechat should be initialled after redis
    wechat.init_app(app)
