#!/bin/bash
authbind gunicorn --bind 0.0.0.0 --reload wsgi:application --access-log=accesslog = './gunicorn.access.log'