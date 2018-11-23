import hashlib
import hmac
import time

from flask import Blueprint, Response
from flask import current_app, jsonify, request, g
from git import Repo

github = Blueprint('webhook', __name__, url_prefix='/github')

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
        current_app.logger.getChild("Github").info('Repository updated with commit {}'.format(commit))
        
    return jsonify({}), 200
