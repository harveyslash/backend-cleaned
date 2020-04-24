"""
Routes mapping for api version 0.1. This allows for nestable
routing. Sub controllers under api v0.1. need to be
'registered' by importing them. The sub controllers need to
import the base blue-print from this file in order to be registered.
"""
from Sugar import JSONifiedNestableBlueprint
from controllers.apiv01.Corporates.Corporates import corporates_controller
from extensions import celery
from models import TestAttempt
from models.SixteenPReport import SixteenPReport
from .Colleges import colleges_controller
from .Courses import courses_controller
from .Discourse import discourse_blueprint
from .Misc import misc_controller
from .Orders import orders_controller
from .PromoCodes import promo_codes_controller
from .Tests import tests_controller
from .Users import user_controller

__author__ = "Harshvardhan Gupta"

base_blueprint = JSONifiedNestableBlueprint("BASE", __name__)

# base_blueprint.register_blueprint(admin_base_blueprint, url_prefix='/admin')
base_blueprint.register_blueprint(user_controller)
base_blueprint.register_blueprint(tests_controller)
base_blueprint.register_blueprint(promo_codes_controller)
base_blueprint.register_blueprint(colleges_controller)
base_blueprint.register_blueprint(orders_controller)
base_blueprint.register_blueprint(courses_controller)
base_blueprint.register_blueprint(discourse_blueprint)
base_blueprint.register_blueprint(misc_controller)
base_blueprint.register_blueprint(corporates_controller)

from flask import request, url_for


@base_blueprint.route('', methods=['Post', 'Get'])
def echo_time():
    """
    Just a function to echo current time.
    May be useful for testing if servers are up.
    :return: current date
    """

    return SixteenPReport.generate_report(12461)


    # test = Person(request.json)
    # print(test)
    # print(test.validate())
    # print(test.to_native())
    # a = [i for i in range(100)]
    # print(a)
    # return
    #
    # return a, 300
    # print(request.json)
    # print(request.form.get('test'))
    # print(request.files['test'])
    # print(request.form.get('body'))
    # return request.form.get('file')
    # return request.form.to_dict()

    # print(request.files)
    # print(request.json)
    return {'ip': request.remote_addr}
    # return {"current_location": "v01/"}


import time

from flask import current_app


@celery.task()
def add_numer():
    return
