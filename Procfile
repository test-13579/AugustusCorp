web: gunicorn augustuscorp.wsgi --workers 2 --timeout 120 --log-file -
release: python3 manage.py collectstatic --noinput && python3 manage.py migrate --noinput
