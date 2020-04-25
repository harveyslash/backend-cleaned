from flask_admin import BaseView, expose, AdminIndexView

from beatest_flask_admin import helpers
from models import TestAttempt, Test, College, User, Section, QuestionSection, Order , OrderTest, Question
from datetime import datetime
from sqlalchemy import and_ , or_
from sqlalchemy.orm import contains_eager, load_only, relationship
from sqlalchemy import func, select , case
from .helpers import is_accessible
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import false
from flask_login import current_user
from flask import request


class Dashboard(AdminIndexView):

    def is_accessible(self):

            return helpers.is_accessible()


    @expose('/')
    def index(self):
        systemdate = datetime.date(datetime.now())
        query1 = TestAttempt.query\
            .filter(TestAttempt.date == systemdate).count()

        query2 = TestAttempt.query\
            .filter(and_(TestAttempt.is_complete == True , TestAttempt.is_graded == False)).count()

        query3 = User.query \
            .join(User.college) \
            .join(User.test_attempts) \
            .options(contains_eager(User.college).load_only(College.college_name)) \
            .options(contains_eager(User.test_attempts).load_only(TestAttempt.id)) \
            .options(load_only(User.id)) \
            .with_entities(TestAttempt.test_id , func.count(TestAttempt.user_id)) \
            .filter(or_(College.college_name.like('Indian Institute of Technology%'), College.college_name.like('IIT%'))).group_by(TestAttempt.test_id).all()


        # query4 = User.query.with_entities(func.count(func.DATE(User.created_date)), func.count(User.is_active == 0)).group_by(User.created_date).all()

        query4 = User.query.with_entities(func.Date(User.created_date), func.count(func.nullif(User.is_active, True)), func.count(func.nullif(User.is_active, False))).group_by(func.Date(User.created_date)).all()

        # query6 = User.query.join(QuestionSection.section).join(Test.sections).options(contains_eager(QuestionSection.section)).options(contains_eager(Test.sections)).with_entities(Test.id, Section.id , QuestionSection.question_id ).all()


        # query6 = Test.query.join(Test.sections).outerjoin(QuestionSection , QuestionSection.section_id== Section.id).outerjoin(Test.orders).with_entities(Test.id,(select([Order.status]).where(case([(Order.status == 'paid' ,1)], else_=0 ))),func.count(Section.id),func.count(QuestionSection.question_id)).group_by(Test.id).all()



        return self.render('FatBoy/Dashboard.html',Count1=query1, Count2=query2, Count3=query3, List=query4)





