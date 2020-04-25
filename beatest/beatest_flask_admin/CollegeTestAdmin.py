from flask_admin.form.rules import BaseRule
from flask_admin.model.form import InlineFormAdmin
from markupsafe import Markup
from wtforms.fields import IntegerField
from wtforms.validators import AnyOf, InputRequired

from models import Section, CollegeTest
from .helpers import BaseAdminView, CKTextAreaField, Link


class CollegeTestAdmin(BaseAdminView):
    column_searchable_list = ['college_id', 'test_id', 'start_date',
        'end_date', 'is_active', 'should_override']

    column_list = column_searchable_list
    column_editable_list = (
        "is_active", 'start_date', 'end_date', "is_active", 'should_override')
