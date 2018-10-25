from flask import Flask
import os 


def create_app():
    # from logging.config import dictConfig

    # dictConfig({
    #     'version': 1,
    #     'formatters': {'default': {
    #         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    #     }},
    #     'handlers': {'wsgi': {
    #         'class': 'logging.StreamHandler',
    #         'stream': 'ext://flask.logging.wsgi_errors_stream',
    #         'formatter': 'default'
    #     }},
    #     'root': {
    #         'level': 'INFO',
    #         'handlers': ['wsgi']
    #     }
    # })



    app = Flask(__name__)
    app.config['GITHUB_SECRET'] = os.environ.get('GITHUB_SECRET')
    app.config['REPO_PATH'] = os.environ.get('REPO_PATH')

    from .base import MyResponse
    app.response_class = MyResponse

    from .wechat import WechatAPI
    app.wechat = WechatAPI(
        os.environ.get("WECHAT_TOKEN"),
        os.environ.get("WECHAT_APP_SECRET"),
        app
        )

    
    from .controller import wechat,github
    app.register_blueprint(wechat)
    app.register_blueprint(github)
    return app
