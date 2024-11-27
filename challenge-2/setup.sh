#!/bin/bash

rm -f /app/db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py init_db --admin /app/flag.txt
rm -f /app/flag.txt