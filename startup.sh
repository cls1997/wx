#!/bin/bash
authbind gunicorn wsgi:application -c ./gunicorn.conf.py