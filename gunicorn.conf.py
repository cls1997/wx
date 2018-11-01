import sys

bind = "0.0.0.0:80"
workers = 1
errorlog = '{}/gunicorn.error.log'.format(sys.path[0])
accesslog = '{}/gunicorn.error.log'.format(sys.path[0])
loglevel = 'debug'