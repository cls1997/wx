#!/bin/bash
<<<<<<< HEAD
authbind gunicorn -c ./gunicorn.conf.py
=======
authbind gunicorn --bind 0.0.0.0 --reload wsgi:application --access-logfile='./gunicorn.access.log'
>>>>>>> 09431946c364fa104b0e463ba882889e4d4b4dd7
