#!/bin/sh
python3.9 init.py
python3.9 -m gunicorn app:app -c gunicorn.conf.py
