from flask_bcrypt import Bcrypt
from flask_celery import Celery
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from flask_caching import Cache

from Mautic import Mautic

db = SQLAlchemy()

migrate = Migrate()

bcrypt = Bcrypt()

mail = Mail()

cors = CORS()

sentry = Sentry()

login_manager = LoginManager()

cache = Cache()

# limiter = Limiter(key_func=get_remote_address,
#                   default_limits=["30 per minute"])

mautic = Mautic()

celery = Celery()

