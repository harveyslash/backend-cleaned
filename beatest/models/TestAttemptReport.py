from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import contains_eager, relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

from Sugar import Dictifiable
from extensions import db, celery
from models.TestAttemptReportPackage.get_analytical_ability import \
    get_analytical_ability
from models.TestAttemptReportPackage.get_conceptual_ability import \
    get_conceptual_ability
from models.TestAttemptReportPackage.get_inference_ability import \
    get_inference_ability
from models.TestAttemptReportPackage.get_mental_math_ability import \
    get_mental_math_ability
from models.TestAttemptReportPackage.get_topic_proficiency import \
    get_topic_proficiency
from models.TestAttemptReportPackage.get_algorithmic_sense import \
    get_algorithmic_sense
from models.TestAttemptReportPackage.get_research_ability import \
    get_research_ability
from models.TestAttemptReportPackage.get_domain_knowledge import \
    get_domain_knowledge
from models.TestAttemptReportPackage.get_coding_sense import \
    get_coding_sense
from models.TestAttemptReportPackage.get_attention_to_detail import \
    get_attention_to_detail
from models.TestAttemptReportPackage.get_creative_thinking import \
    get_creative_thinking
from models.TestAttemptReportPackage.get_integrity_quotient import \
    get_integrity_quotient
from models.TestAttemptReportPackage.get_strategy_and_decision import \
    get_strategy_and_decision
from models.TestAttemptReportPackage.get_people_management import \
    get_people_management

class TestAttemptReport(Dictifiable, db.Model):
    __tablename__ = 'test_attempt_report'

    test_attempt_id = Column(Integer,
                             ForeignKey('test_attempt.id', ondelete="CASCADE"),
                             primary_key=True)

    conceptual_level = Column(Float)
    inference_level = Column(Float)
    analytical_ability = Column(Float)
    mental_math_speed = Column(Float)
    algorithmic_sense = Column(Float)
    research_ability = Column(Float)
    domain_knowledge = Column(Float)
    coding_sense = Column(Float)
    coding_quality = Column(Float)

    attention_to_detail = Column(Float)
    creative_thinking = Column(Float)
    integrity_quotient = Column(Float)
    strategy_and_decision = Column(Float)
    people_management = Column(Float)

    # these are question broad topics
    data_interpretation_ability = Column(Float)
    domain_based_ability = Column(Float)
    logical_reasoning_ability = Column(Float)
    paragraph_writing_ability = Column(Float)
    verbal_ability = Column(Float)
    verbal_reasoning = Column(Float)




    is_finished = Column(Boolean, nullable=False, default=False)

    create_date = Column(DateTime, server_default=func.now())
    last_update_date = Column(DateTime, onupdate=func.now())
    finish_date = Column(DateTime)

    test_attempt = relationship("TestAttempt",
                                back_populates="report",
                                uselist=False)

    @staticmethod
    @celery.task()
    def generate_report(test_attempt_id):
        print(test_attempt_id)
        from models import (TestAttempt, QuestionAttempt)
        from models import SectionAttempt, Question

        data = (
            TestAttempt
                .query
                .filter(TestAttempt.id == test_attempt_id)
                .join(TestAttempt.test)
                .join(TestAttempt.section_attempts)
                .join(SectionAttempt.question_attempts)
                .join(QuestionAttempt.question)
                .join(Question.tags)
                .options(
                    contains_eager(TestAttempt.section_attempts)
                        .contains_eager(SectionAttempt.question_attempts)
                        .contains_eager(QuestionAttempt.question)
                        .contains_eager(Question.tags)
            )
                .one()
        )

        new = False

        try:

            report = TestAttemptReport.query.filter(
                    TestAttemptReport.test_attempt_id == test_attempt_id).one()
        except NoResultFound:
            report = TestAttemptReport(test_attempt_id=test_attempt_id)
            new = True

        data_dict = data.todict()
        report.analytical_ability = get_analytical_ability(data_dict)
        report.conceptual_level = get_conceptual_ability(data_dict)
        report.mental_math_speed = get_mental_math_ability(data_dict)
        report.inference_level = get_inference_ability(data_dict)
        report.algorithmic_sense = get_algorithmic_sense(data_dict)
        report.research_ability = get_research_ability(data_dict)
        report.domain_knowledge = get_domain_knowledge(data_dict)
        report.coding_sense = get_coding_sense(data_dict)

        report.attention_to_detail = get_attention_to_detail(data_dict)
        report.creative_thinking = get_creative_thinking(data_dict)
        report.integrity_quotient = get_integrity_quotient(data_dict)
        report.strategy_and_decision = get_strategy_and_decision(data_dict)
        report.people_management = get_people_management(data_dict)

        report.data_interpretation_ability = get_topic_proficiency(
                data_dict,
                "f-5-category-broad topic-data interpretation")

        report.domain_based_ability = get_topic_proficiency(data_dict,
                                                            "f-5-category-broad topic-domain based")

        report.logical_reasoning_ability = get_topic_proficiency(data_dict,
                                                                 "f-5-category-broad topic-logical reasoning")

        report.paragraph_writing_ability = get_topic_proficiency(data_dict,
                                                                 "f-5-category-broad topic-paragraph wiritng")

        report.verbal_ability = get_topic_proficiency(data_dict,
                                                      "f-5-category-broad topic-verbal ability")

        report.verbal_reasoning = get_topic_proficiency(data_dict,
                                                        "f-5-category-broad topic-verbal reasoning")

        if new:
            db.session.add(report)

        db.session.commit()

        return data
