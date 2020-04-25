from flask_admin import expose
from flask_admin.model.template import EndpointLinkRowAction, LinkRowAction
from flask_login import login_user

from beatest_flask_admin.helpers import BaseAdminView
from controllers.rex import CookieHelper
from models import User


class UserAdmin(BaseAdminView):
    # def is_visible(self):
    #     return False

    column_list = ['id', 'full_name', 'email']
    column_searchable_list = ('id', "full_name", 'email')
    column_filters = ("id", "full_name", "email")

    form_create_rules = ('email', "is_active")
    form_edit_rules = ('email', "is_active")

    column_extra_row_actions = [
        EndpointLinkRowAction('glyphicon glyphicon-user', 'user.action_play',
                              title="Login as User"),
    ]

    @expose('impersonate/<id>', methods=('Get',))
    def action_play(self, *args, **kwargs):
        user = User.query.get(kwargs['id'])
        login_user(user)

        if user.corporate != None:
            corporate_id = user.corporate.id
            CookieHelper.set_corporate_cookie(corporate_id)
        return self.handle_action()
