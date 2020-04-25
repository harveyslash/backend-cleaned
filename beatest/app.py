"""
App setup and configuration.
This sets up different fixers,wrappers
and also several extensions that are required by the app.
It also sets up the routes related to the app.
"""
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from raven import Client
from raven.contrib.celery import register_signal

from beatest_flask_admin.Dashboard import Dashboard
from controllers.UI import routes as UI_routes

__author__ = "harshvardhan gupta"

from flask_admin import Admin
# from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from Sugar import Flask, ModelJSONEncoder, setup_error_handlers, \
    setup_login_manager
from beatest_flask_admin.AdminSetup import flask_admin_setup
from controllers.apiv01 import routes as apiv01_routes
from controllers.rex import routes as rex_routes
from extensions import *
from aws_xray_sdk.core import xray_recorder


def configure_imports():
    import schedules.update_college_test_table

    schedules.no_task()



def configure_wrappers(app):
    """
    Configure wrappers.
    Meant for wrappers or fixers that work on the app itself.
    This includes custom error handlers, etc.

    :param app:
    :return:
    """

    app.json_encoder = ModelJSONEncoder

    app.wsgi_app = ProxyFix(
            app.wsgi_app,
            num_proxies=app.config['NUM_PROXIES'],
    )

    setup_error_handlers(app)


def create_app(config_file_name='./configs/prod.py'):
    """
    Create the instance of the app after configuring all extensions

    :return: the app instance and the manager instance
    """
    app = Flask(__name__, static_url_path='/statics', static_folder='static/')
    app.config.from_pyfile(config_file_name)

    configure_extensions(app)
    configure_blueprints(app)
    configure_wrappers(app)

    return app


def configure_extensions(app):
    """
    Configure extensions of the app.
    Add additional extensions in this functions if you need to add
    more flask extensions

    :param app: the app that will attach to the extensions
    :return: None
    """

    cors.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mautic.init_app(app)

    # flask admin setup
    ###########################
    f_admin = Admin(
            app,
            url="/api/admin",
            name='Admin',
            template_mode="bootstrap3",
            index_view=Dashboard(name='Home',
                                 url="/api/admin",
                                 )
    )
    flask_admin_setup(f_admin, app)
    ###########################

    cache.init_app(app, app.config)

    # limiter.init_app(app)

    if not app.debug:
        sentry.init_app(app)

        client = Client(
                app.config['SENTRY_DSN'])

        register_signal(client)
        # patch_all()
        xray_recorder.configure(
                service="beatest-api-v0.1",
                sampling=False,
                context_missing='LOG_ERROR',
                daemon_address='127.0.0.1:2000',
                dynamic_naming='*beatest.in*'
        )

        XRayMiddleware(app, xray_recorder)

    setup_login_manager(login_manager)

    celery.init_app(app)

    configure_imports()


def configure_blueprints(app):
    """
    Set up all blueprints required for the app

    :param app: the app to which the blueprints will be attached
    :return:
    """

    app.register_blueprint(
            apiv01_routes.base_blueprint, url_prefix="/api/v0.1"
    )

    app.register_blueprint(
            rex_routes.base_blueprint, url_prefix="/api/rex"
    )

    app.register_blueprint(
            UI_routes.base_blueprint, url_prefix="/"
    )

