from flask_admin.actions import action
from flask_admin.form.rules import BaseRule
from flask_admin.model.form import InlineFormAdmin
from markupsafe import Markup
from sqlalchemy.orm import contains_eager, load_only
from wtforms.fields import IntegerField
from wtforms.validators import AnyOf, InputRequired

from extensions import celery
from models import Section, TestAttempt
from .helpers import BaseAdminView, CKTextAreaField, Link


class TestAttemptAdmin(BaseAdminView):
    column_searchable_list = (
        'id', 'user.full_name', 'test_id', 'test.name', 'user_id',
        'is_complete',
        'is_graded', 'score',
        'date')

    column_list = column_searchable_list
    can_export = True

    column_filters = column_searchable_list
    column_sortable_list = column_searchable_list

    @action('approve', 'Mark Complete',
            'Are you sure you want to complete these tests?')
    def action_approve(self, ids):
        for id in ids:
            complete_test_attempt.delay(id)


@celery.task()
def complete_test_attempt(test_attempt_id):
    test_attempt = (TestAttempt.query
                    .filter(TestAttempt.id == test_attempt_id)
                    .options(
            load_only(TestAttempt.user_id, TestAttempt.test_id))
                    .one()
                    )

    TestAttempt.calculate_score_for_test(test_attempt.user_id,
                                         test_attempt.test_id,
                                         should_persist=True)
