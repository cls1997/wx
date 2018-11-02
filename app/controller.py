import hashlib
import hmac
import time

from flask import Blueprint, Response
from flask import current_app, jsonify, request, g
from git import Repo

github = Blueprint('webhook', __name__, url_prefix='/github')
wechat = Blueprint('wechat', __name__, url_prefix='/wechat')


@wechat.before_request
def before_request():
    g.start_time = time.time()


@wechat.teardown_request
def teardown_request(exception = None):
    diff = time.time() - g.start_time
    current_app.logger.info(
        "It spent %dms to handle this request.", int(1000*diff))


@wechat.route("", methods=['POST'])
def handle_post():
    post_data = request.data.decode(encoding="utf-8", errors="strict")
    return Response(current_app.wechat.handle_message(post_data),
                    mimetype='application/xml')


@wechat.route("", methods=['GET'])
def handle_get():
    params = request.args
    signature = params.get("signature", "")
    timestamp = params.get("timestamp", "")
    nonce = params.get("nonce", "")
    echostr = params.get("echostr", "")

    if (current_app.wechat.check_signature(signature, timestamp, nonce)):
        return echostr

    if(current_app.debug):
        return "DEBUG"
    else:
        return ""


@github.route('', methods=['POST'])
def handle_github_hook():
    """ Entry point for github webhook """
    signature = request.headers.get('X-Hub-Signature')
    _, signature = signature.split('=')
    secret = str.encode(current_app.config.get('GITHUB_SECRET'))
    hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
    if hmac.compare_digest(hashhex, signature):
        repo = Repo(current_app.config.get('REPO_PATH'))
        origin = repo.remotes.origin
        origin.pull()
        commit = request.json['after'][0:6]
        current_app.logger.info('Repository updated with commit {}'.format(commit))
        
    return jsonify({}), 200
