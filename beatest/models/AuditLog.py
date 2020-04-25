import enum

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, JSON, \
    Sequence, func, String

from Sugar import Dictifiable
from extensions import db


class AuditLogActionType(enum.Enum):
    question_attempt_modified = 'question_attmpt_modified'
    focus_change_event = 'focus_change'
    start_test_event = 'start_test'


class AuditLog(Dictifiable, db.Model):
    id = Column(BigInteger, Sequence('audit_log_id_seq'), primary_key=True)

    user_id = Column(Integer,
                     ForeignKey('user.id'),
                     nullable=True)

    json = Column(JSON, nullable=True)

    date = Column(DateTime, nullable=False,
                  server_default=func.now())

    action_type = Column(String(500), nullable=False)
    extra = Column(JSON, nullable=True)

    @staticmethod
    def log_question_attempt_update(user_id,
                                    test_id,
                                    section_id,
                                    question_id,
                                    modified_key_vals):
        log = AuditLog(user_id=user_id,
                       action_type=AuditLogActionType.question_attempt_modified.value,
                       json={'action': modified_key_vals,
                           'test_id': test_id,
                           'section_id': section_id,
                           'question_id': question_id}
                       )

        db.session.add(log)
        db.session.commit()

    @staticmethod
    def log_focus_change_event(user_id, test_id):
        log = AuditLog(user_id=user_id,
                       action_type=AuditLogActionType.focus_change_event.value,
                       json={
                           'test_id': test_id
                       }
                       )

        db.session.add(log)
        db.session.commit()

    @staticmethod
    def log_start_test_event(user_id, test_id, current_section_id):
        log = AuditLog(user_id=user_id,
                       action_type=AuditLogActionType.start_test_event.value,
                       json={
                           'test_id': test_id,
                           'current_section_id': current_section_id
                       }
                       )

        db.session.add(log)
        db.session.commit()
