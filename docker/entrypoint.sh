#!/bin/sh

# 1. 마이그레이션 실행
echo ">>>>>> Running migrations"
python manage.py migrate

# 2. 이후 커맨드 실행 (runserver, gunicorn 등)
exec "$@"
