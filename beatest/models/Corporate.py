from sqlalchemy import Column, Integer, \
    Sequence, String, and_
from sqlalchemy.orm import load_only, contains_eager

from Sugar import Dictifiable
from extensions import db
from models import College
import dateutil.parser

import dateutil.relativedelta
from datetime import datetime


class Corporate(Dictifiable, db.Model):
    __tablename__ = 'corporate'

    id = Column(Integer, Sequence('corporate_id_seq'), primary_key=True)
    name = Column(String(1024), nullable=False)
    slug = Column(String(1024), unique=True)
    logo = Column(String(1024), nullable=True)
    url = Column(String(1024), nullable=True)

    admins = db.relationship('User', secondary='corporate_admin')
    tests = db.relationship('Test', secondary='corporate_test')
    applicants = db.relationship('User', secondary='corporate_applicants')

    corporate_applicants = db.relationship("CorporateApplicants",
                                           back_populates='corporate',
                                           uselist=False)

    @staticmethod
    def can_access_test(corporate_id: int, test_id: int):
        from models import CorporateTest

        corporate_test_exists = (db.session.query(
                CorporateTest.query
                    .filter(CorporateTest.test_id == test_id)
                    .filter(CorporateTest.corporate_id == corporate_id)
                    .exists())
                                 .scalar())

        return corporate_test_exists

    @staticmethod
    def can_access_user(corporate_id: int, user_id: int):
        from models import CorporateTest, CorporateApplicants

        corporate_test_exists = (db.session.query(
                CorporateApplicants.query
                    .filter(CorporateApplicants.user_id == user_id)
                    .filter(CorporateApplicants.corporate_id == corporate_id)
                    .exists())
                                 .scalar())

        return corporate_test_exists

    @staticmethod
    def get_personality_analysis(corporate_id, test_id, date):
        """
        Get the test attempt -> section attempt data of all users
        who are mapped in the corporate_applicants table

        :param corporate_id:
        :param test_id:
        :return: an array of test attempts along with each test attempts'
                section attempts
        """
        from models import (TestAttempt, User, CorporateApplicants,
                            SectionAttempt, Test, Question)
        date = dateutil.parser.parse(date).date()
        plus_one_day = dateutil.relativedelta.relativedelta(days=+1)

        return (Test.query
                .filter(Test.id == test_id)
                .outerjoin(TestAttempt, and_(TestAttempt.test_id == test_id,
                                             TestAttempt.date > date + plus_one_day,
                                             TestAttempt.date <
                                             date + plus_one_day + plus_one_day,
                                             TestAttempt.user_id.in_(
                                                     db.session.query(
                                                             CorporateApplicants.user_id)
                                                         .filter(
                                                             CorporateApplicants.corporate_id == corporate_id)
                                             )

                                             ))
                .outerjoin(TestAttempt.sixteen_p_report)
                .options(contains_eager(Test.test_attempts)
                         .contains_eager(TestAttempt.sixteen_p_report))
                .one()
                )

    @staticmethod
    def get_qualitative_analysis(corporate_id, test_id, date):
        """
        Get the test attempt -> section attempt data of all users
        who are mapped in the corporate_applicants table

        :param corporate_id:
        :param test_id:
        :return: an array of test attempts along with each test attempts'
                section attempts
        """
        from models import (TestAttempt, User, CorporateApplicants,
                            SectionAttempt, Test, Question)
        date = dateutil.parser.parse(date).date()
        plus_one_day = dateutil.relativedelta.relativedelta(days=+1)

        return (Test.query
                .filter(Test.id == test_id)
                .outerjoin(TestAttempt, and_(TestAttempt.test_id == test_id,
                                             TestAttempt.date > date + plus_one_day,
                                             TestAttempt.date <
                                             date + plus_one_day + plus_one_day,
                                             TestAttempt.user_id.in_(
                                                     db.session.query(
                                                             CorporateApplicants.user_id)
                                                         .filter(
                                                             CorporateApplicants.corporate_id == corporate_id)
                                             )

                                             ))
                .outerjoin(TestAttempt.report)
                .options(contains_eager(Test.test_attempts)
                         .contains_eager(TestAttempt.report))
                .one()
                )

    @staticmethod
    def get_tab_change(corporate_id, test_id, date):
        """
        Get the focus_lost_count for each test attempt of all users
        who are mapped in the corporate_applicants table

        :param corporate_id:
        :param test_id:
        :return: an array of focus_lost_count for the test
        """
        from models import (TestAttempt, User, CorporateApplicants,
                            SectionAttempt, Test, Question)
        date = dateutil.parser.parse(date).date()
        plus_one_day = dateutil.relativedelta.relativedelta(days=+1)

        return (Test.query
                .filter(Test.id == test_id)
                .outerjoin(TestAttempt, and_(TestAttempt.test_id == test_id,
                                             TestAttempt.date > date + plus_one_day,
                                             TestAttempt.date <
                                             date + plus_one_day + plus_one_day,
                                             TestAttempt.user_id.in_(
                                                 db.session.query(
                                                     CorporateApplicants.user_id)
                                                     .filter(
                                                     CorporateApplicants.corporate_id == corporate_id)
                                             )

                                             ))
                .options(contains_eager(Test.test_attempts).load_only(TestAttempt.focus_lost_count))
                .one()
                )

    @staticmethod
    def get_test_performance(corporate_id, test_id, date):
        """
        Get the test attempt -> section attempt data of all users
        who are mapped in the corporate_applicants table

        :param corporate_id:
        :param test_id:
        :return: an array of test attempts along with each test attempts'
                section attempts
        """
        from models import (TestAttempt, User, CorporateApplicants,
                            SectionAttempt, Test, Question)
        date = dateutil.parser.parse(date).date()
        plus_one_day = dateutil.relativedelta.relativedelta(days=+1)

        return (Test.query
                .filter(Test.id == test_id)
                .join(Test.sections)
                # .join(Section.questions)
                .outerjoin(TestAttempt, and_(TestAttempt.test_id == test_id,
                                             TestAttempt.date > date + plus_one_day,
                                             TestAttempt.date <
                                             date + plus_one_day + plus_one_day,
                                             TestAttempt.user_id.in_(
                                                     db.session.query(
                                                             CorporateApplicants.user_id)
                                                         .filter(
                                                             CorporateApplicants.corporate_id == corporate_id)
                                             )

                                             ))
                .outerjoin(TestAttempt.section_attempts)
                .outerjoin(User)
                .outerjoin(User.application)
                .outerjoin(User.college)
                .options(contains_eager(Test.test_attempts)
                         .contains_eager(TestAttempt.user)
                         .load_only(User.full_name)
                         .contains_eager(User.application)
                         )
                .options(contains_eager(Test.test_attempts)
                         .contains_eager(TestAttempt.user)
                         .contains_eager(User.college)
                         .load_only(College.college_name))
                .options(contains_eager(Test.test_attempts)
            .contains_eager(
                TestAttempt.section_attempts))

                .options(contains_eager(Test.sections)
                         )
                # .contains_eager(Section.questions)
                # .load_only(Question.lod, Question.topic,
                #            Question.type))
                # )

                .one()
                )

        return (Test.query
                .filter(Test.id == test_id)
                .join(Test.sections)
                # .join(Section.questions)
                .outerjoin(TestAttempt, and_(TestAttempt.test_id == test_id,
                                             TestAttempt.user_id.in_(
                                                     db.session.query(
                                                             CorporateApplicants.user_id)
                                                         .filter(
                                                             CorporateApplicants.corporate_id == corporate_id)
                                             )))
                .outerjoin(TestAttempt.section_attempts)
                .outerjoin(User)
                .options(contains_eager(Test.test_attempts)
                         .contains_eager(TestAttempt.user)
                         .load_only(User.full_name))
                .options(contains_eager(Test.test_attempts)
            .contains_eager(
                TestAttempt.section_attempts))

                # .options(contains_eager(Test.sections)
                # .contains_eager(Section.questions)
                # .load_only(Question.lod, Question.topic,
                #            Question.type))
                # )

                .one()
                )
