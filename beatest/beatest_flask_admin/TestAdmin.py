from flask_admin.form.rules import BaseRule
from flask_admin.model.form import InlineFormAdmin
from markupsafe import Markup
from wtforms.fields import IntegerField
from wtforms.validators import AnyOf, InputRequired

from models import Section
from .helpers import BaseAdminView, CKTextAreaField, Link


class SectionInlineForm(InlineFormAdmin):
    form_columns = (
        'name', 'should_randomize_questions', 'id', 'total_time',
        'created_date')
    form_rules = (
        'name',
        'should_randomize_questions',
        'total_time',
        'created_date',
        Link(endpoint='section.edit_view',
             attribute='id',
             text="Edit Questions"))

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


class TestLogoPreview(BaseRule):
    def __init__(self, attribute):
        super(TestLogoPreview, self).__init__()
        self.attribute = attribute

    def __call__(self, form, form_opts=None, field_args={}):
        logo = None if form._obj is None else form._obj.logo

        return Markup(
                f"<img src='https://beatest.in{logo}'/>")


class TestAdmin(BaseAdminView):
    column_searchable_list = ('name',)

    column_list = ['name']

    form_overrides = dict(instruction_html=CKTextAreaField)

    form_edit_rules = ['name',
        'is_active',
        'allow_section_jumps',
        'logo',
        TestLogoPreview('logo'),
        'type',
        'character',
        'price',
        'created_date',
        'instruction_html',
        'sections',
    ]
    form_create_rules = form_edit_rules

    inline_models = (SectionInlineForm(Section),)

    form_choices = {
        'character': [
            ('Mock', 'Mock'),
            ('Topic', 'Topic'),
        ],

        'type': [
            ('SBI', 'SBI'),
            ('CAT', 'CAT'),
            ('IBPS', 'IBPS'),
            ('COLLEGE', 'COLLEGE'),
        ]
    }

    form_args = {
        'name': {
            'validators': [InputRequired()]
        },
        'type': {
            'validators': [InputRequired(),
                AnyOf(['SBI', 'CAT', 'IBPS', 'COLLEGE'])]
        },
        'character': {
            'validators': [InputRequired(), AnyOf(['Mock', 'Topic'])]
        },
        'price': {
            'validators': [InputRequired(), IntegerField]
        },
        'created_date': {
            'validators': [InputRequired()]

        }
    }
