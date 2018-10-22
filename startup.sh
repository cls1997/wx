#!/bin/bash

gunicorn --bind 0.0.0.0 --reload wsgi:application