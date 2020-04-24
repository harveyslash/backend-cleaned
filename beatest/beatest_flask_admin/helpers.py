"""
Set of helper functions for flask admin.
"""
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin

__author__ = "harshvardhan gupta"
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.rules import BaseRule
from flask_login import current_user
from jinja2 import Markup
from wtforms import TextField
from wtforms.widgets import TextArea

from extensions import db
from models import Role, UserRoles


def is_accessible():
    if not current_user.is_authenticated:
        return False

    current_user_id = current_user.id

    query = UserRoles.query.join(UserRoles.role) \
        .filter(Role.name == 'admin') \
        .filter(UserRoles.user_id == current_user_id) \
        .exists()

    return db.session.query(query).scalar()


class CKTextAreaWidget(TextArea):
    """
    A custom widget to use ckeditor
    as the editor.
    """

    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextField):
    """
    Text area field that sets the widget to cktextareawidget
    """
    widget = CKTextAreaWidget()


class Link(BaseRule):
    """
    HTML Link to a related model's edit pages.

    """

    def __init__(self, endpoint, attribute, text):
        """

        :param endpoint: Which model to link to
        :param attribute: Which attribute of the model
                        (i.e. the id of the related model)
        :param text:  The text to display at the link
        """
        super(Link, self).__init__()
        self.endpoint = endpoint
        self.text = text
        self.attribute = attribute

    def __call__(self, form, form_opts=None, field_args={}):
        _id = getattr(form._obj, self.attribute, None)

        if _id:
            return Markup('<a href="{url}">{text}</a>'.format(
                    url=url_for(self.endpoint, id=_id), text=self.text))


class MultiLink(BaseRule):
    def __init__(self, endpoint, relation, attribute):
        super(MultiLink, self).__init__()
        self.endpoint = endpoint
        self.relation = relation
        self.attribute = attribute

    def __call__(self, form, form_opts=None, field_args={}):
        _hrefs = []
        _objects = getattr(form._obj, self.relation)
        for _obj in _objects:
            _id = getattr(_obj, self.attribute, None)
            _link = '<a href="{url}">Edit {text}</a>'.format(
                    url=url_for(self.endpoint, id=_id), text=str(_obj.id))
            _hrefs.append(_link)

        return Markup('<br>'.join(_hrefs))


class BaseAdminView(ModelView):
    """
    Base view for admin.
    This just adds admin access checks and sets the template to use
    """

    def is_accessible(self):
        return is_accessible()

    create_template = 'FatBoy/adminBase.html'
    edit_template = 'FatBoy/adminBase.html'

    action_disallowed_list = ['delete']


class ProtectedS3FileAdmin(S3FileAdmin):

    def is_accessible(self):
        return is_accessible()
