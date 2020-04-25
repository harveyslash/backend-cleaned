"""
Routes mapping for UI. This allows for nestable
routing. Sub controllers under api v0.1. need to be
'registered' by importing them. The sub controllers need to
import the base blue-print from this file in order to be registered.
"""
from flask import Flask, url_for, render_template, make_response, request
from Sugar import JSONifiedNestableBlueprint
from flask import url_for, render_template, make_response, jsonify
from models import TestAttempt, Test, Section, QuestionSection, Order , OrderTest, Question
from sqlalchemy import func, select , case
from Sugar import JSONifiedNestableBlueprint
from flask import request
from flask_login import current_user, login_required
from sqlalchemy import and_
from sqlalchemy.orm import contains_eager, load_only

from flask import jsonify
import requests

__author__ = "Harshvardhan Gupta"
base_blueprint = JSONifiedNestableBlueprint("UIBASE", __name__)


@base_blueprint.route('/', methods=['Get'])
def status_page():
    """
    Just a function to echo current time.
    May be useful for testing if servers are up.
    :return: current date
    """
    r = make_response(render_template("UI/Pages/landing_page.html"))
    return r


@base_blueprint.route('/test', methods=['GET', 'POST'])
def test_listing():

    """
    Just a function to echo current time.
    May be useful for testing if servers are up.
    :return: current date
    """

    current_user_id = current_user.id if not current_user.is_anonymous else None

    tests = (Test.query
             .filter_by(**request.args)
             .outerjoin(Test.sections)
             .outerjoin(Section.questions)
             .outerjoin(OrderTest,
                        OrderTest.test_id == Test.id)
             .outerjoin(Order, and_(Order.id == OrderTest.order_id,
                                    Order.user_id == current_user_id))
             .outerjoin(TestAttempt, and_(
        TestAttempt.test_id == Test.id,
        TestAttempt.is_complete == 1,
        TestAttempt.user_id == current_user_id
    ))
             .options(contains_eager(Test.sections)
                      .load_only(Section.id, Section.total_time)
                      .contains_eager(Section.questions)
                      .load_only(Question.id))
             .options(contains_eager(Test.test_attempts)
                      .load_only(TestAttempt.is_complete)
                      )
             .options(
        load_only(Test.id, Test.name, Test.character, Test.price,
                  Test.type, Test.logo, Test.allow_section_jumps))
             .options(contains_eager(Test.orders)
                      .load_only(Order.status))
             .filter(Test.is_active == 1)
             .all())

    fields = ['id',
              'name',
              'character',
              'allow_section_jumps',
              'price',
              'logo',
              'orders',
              'sections',
              {'sections': ['id', 'total_time', 'questions', {'questions': 'id'}]},
              'type',
              'test_attempts',
              {'orders':
                   ['status']
               },
              {'test_attempts':
                   ['is_complete']}
              ]
    tests = [test.todict(fields) for test in tests]
    for test in tests:
        test['is_purchased'] = False  # set key, false by default
        #if len(test['orders']) > 0:  # if a paid order exists
        #   test['is_purchased'] = True  # set is purchased to true
        for order in test['orders']:
            test['status'] = order['status']
            if order['status'] == "paid":
                test['is_purchased'] = True
        del test['orders']

        test['is_complete'] = False  # set key , false by default

        if len(test['test_attempts']):
            test['is_complete'] = True

        del test['test_attempts']

        question_count = 0
        section_count = 0

        total_time = 0
        for section in test["sections"]:
            section_count += 1
            total_time += section['total_time']

            for question in section["questions"]:
                question_count += 1

        test['section_count'] = section_count
        test['question_count'] = question_count
        test['total_time'] = total_time

        del test['sections']


    r = make_response(render_template("UI/Pages/test_listing.html"))
    return r


@base_blueprint.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    r = make_response(render_template("UI/Pages/forget_password.html"))
    return r
# <<<<<<< HEAD

# =======
# >>>>>>> 95f7c82b5360447755829f66c7ccfaeb799b17c7

@base_blueprint.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification():
    r = make_response(render_template("UI/Pages/resend_verification.html"))
    return r


@base_blueprint.route('/login')
def log_in():
    r = make_response(render_template("UI/Pages/log_in.html"))
    return r


@base_blueprint.route('/signup', methods=['GET', 'POST'])
def sign_up():
    r = make_response(render_template("UI/Pages/sign_up.html"))
    return r

@base_blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    r = make_response(render_template("UI/Pages/reset_password.html"))
    return r


@base_blueprint.route('/profile-form', methods=['GET', 'POST'])
def profile_forms():
    r = make_response(render_template("UI/Pages/profile_forms.html"))
    return r


@base_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    r = make_response(render_template("UI/Pages/dashboard.html"))
    return r