#!/bin/bash

gunicorn --bind 0.0.0.0:40621 --reload wsgi:application