from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.model.form import InlineFormAdmin
from wtforms.fields import IntegerField
from wtforms.validators import InputRequired

from extensions import db
from models import Question
from .helpers import BaseAdminView, Link
from flask_admin.form.rules import Field, HTML, Text


class QuestionInlineForm(InlineFormAdmin):
    form_columns = ('id', 'points_correct', 'points_wrong', 'html')
    form_rules = ('points_correct', 'points_wrong',

    Field('html'),
    Link(endpoint='question.edit_view',
         attribute='id',
         text='Edit Question in Detail'),

    )

    form_args = {
        'points_correct': {
            'validators': [InputRequired(), IntegerField]
        },
        'points_wrong': {
            'validators': [InputRequired(), IntegerField]
        },

    }


class SectionAdmin(BaseAdminView):

    def is_visible(self):
        return True

    column_list = ['name', 'total_time', 'created_date']
    column_searchable_list = column_list

    form_edit_rules = [
        'name',
        'should_randomize_questions',
        'total_time',
        'created_date',
        'questions'
    ]

    inline_models = (QuestionInlineForm(Question),)

    form_args = {
        'name': {
            'validators': [InputRequired()]
        },
        'total_time': {
            'validators': [InputRequired(), IntegerField]
        },
        'created_date': {
            'validators': [InputRequired()]
        }
    }
