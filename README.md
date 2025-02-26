# DRP-Test applications
Main branch - Startup command for app service - uvicorn app:app --host 0.0.0.0 --port 8000
flask-db branch - flask application startup cmd - gunicorn --bind 0.0.0.0:8000 app:app
