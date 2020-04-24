"""
This module adds columns dynamically to models.
It needs to be done in this fashion to prevent any cyclic imports that might
occur.

"""

from sqlalchemy import func, select
from sqlalchemy.orm import column_property

from models import QuestionAttempt, SectionAttempt

SectionAttempt.total_question_count = column_property(select([func.count()],
                                                               QuestionAttempt.section_attempt_id
                                                               == SectionAttempt.__table__.c.id
                                                             ).correlate(
        SectionAttempt.__table__).as_scalar(),
                                                      deferred=True)
