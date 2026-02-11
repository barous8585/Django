web: gunicorn tontine_digitale.wsgi --log-file -
release: python manage.py migrate --no-input && python manage.py collectstatic --no-input
