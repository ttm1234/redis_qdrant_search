#!/bin/sh
python3.9 init.py
gunicorn app:app -c gunicorn.conf.py
