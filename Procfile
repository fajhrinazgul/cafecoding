web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker cafecoding.asgi:application
release: python manage.py migrate