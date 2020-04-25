from sqlalchemy import Column, Float, ForeignKey, Integer, \
    String, Text, and_
from sqlalchemy.orm import contains_eager, load_only, relationship
from sqlalchemy.orm.exc import NoResultFound

from Sugar import Dictifiable
from extensions import celery, db


class SixteenPReport(Dictifiable, db.Model):
    __tablename__ = 'sixteen_p_report'

    test_attempt_id = Column(Integer,
                             ForeignKey('test_attempt.id', ondelete="CASCADE"),
                             primary_key=True)

    personality_type = Column(String(512))
    role = Column(String(512))
    strategy = Column(String(512))

    mind_value = Column(Float)
    mind_text = Column(Text)

    energy_value = Column(Float)
    energy_text = Column(Text)

    nature_value = Column(Float)
    nature_text = Column(Text)

    tactics_value = Column(Float)
    tactics_text = Column(Text)

    identity_value = Column(Float)
    identity_text = Column(Text)

    test_attempt = relationship("TestAttempt",
                                back_populates="sixteen_p_report",
                                uselist=False)

    @staticmethod
    @celery.task()
    def generate_report(test_attempt_id):
        from models import Question
        from models import QuestionAttempt
        from models import SectionAttempt
        from models import Choice
        from Algos.SixteenP import scraping

        question_attempts = (QuestionAttempt.query
                             .join(QuestionAttempt.question)
                             .outerjoin(Question.choices)
                             .join(SectionAttempt,
                                   and_(
                                           SectionAttempt.id == QuestionAttempt.section_attempt_id,
                                           SectionAttempt.test_attempt_id == test_attempt_id))

                             .options(load_only(QuestionAttempt.choice_id))
                             .options(contains_eager(QuestionAttempt.question)
                                      .load_only(Question.id)
                                      .contains_eager(Question.choices)
                                      .load_only(Choice.id))
                             .all()
                             )

        scrapped_info = scraping.scrape(question_attempts)

        if scrapped_info is None:
            return

        try:
            report = SixteenPReport.query.filter(
                    SixteenPReport.test_attempt_id == test_attempt_id).one()
            db.session.delete(report)


        except NoResultFound:
            pass
        report = SixteenPReport(test_attempt_id=test_attempt_id,
                                **scrapped_info)
        db.session.add(report)
        db.session.commit()

        return question_attempts
