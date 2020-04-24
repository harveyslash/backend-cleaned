import warnings

from beatest_flask_admin.CollegeTestAdmin import CollegeTestAdmin
from beatest_flask_admin.Dashboard import Dashboard
from flask import current_app
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin

from flask_admin import BaseView, expose
from beatest_flask_admin.CollegeAdmin import CollegeAdmin
from beatest_flask_admin.TagAdmin import TagAdmin
from flask_admin import Admin
from beatest_flask_admin.TestAttemptAdmin import TestAttemptAdmin
from beatest_flask_admin.UserAdmin import UserAdmin
from beatest_flask_admin.helpers import ProtectedS3FileAdmin
from extensions import db
from models import College, Question, Section, Tag, Test, User, TestAttempt, \
    CollegeTest
from .QuestionAdmin import QuestionAdmin
from .SectionAdmin import SectionAdmin
from .TestAdmin import TestAdmin
from datetime import datetime
from flask import render_template


def flask_admin_setup(admin, app):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset',
                                UserWarning)
        admin.add_view(TestAdmin(Test, db.session, category="Exams"))
        admin.add_view(SectionAdmin(Section, db.session, category="Exams"))
        admin.add_view(QuestionAdmin(Question, db.session, category="Exams"))
        admin.add_view(TagAdmin(Tag, db.session, category="Exams"))
        admin.add_view(UserAdmin(User, db.session))
        admin.add_view(CollegeAdmin(College, db.session))

        with app.app_context():
            admin.add_view(ProtectedS3FileAdmin('beatest-blobs',
                                                'ap-south-1',
                                                current_app.config[
                                                    'AWS_ACCESS_KEY'],
                                                current_app.config[
                                                    'AWS_SECRET_KEY'],
                                                name="Files"
                                                )
                           )

        admin.add_view(TestAttemptAdmin(TestAttempt, db.session))
        admin.add_view(CollegeTestAdmin(CollegeTest, db.session))
