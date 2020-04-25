"""
Entry point of the app for WSGI servers like Gunicorn.
"""
from app import create_app

app = create_app()

