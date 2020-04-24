from beatest_flask_admin.helpers import BaseAdminView


class TagAdmin(BaseAdminView):
    # def is_visible(self):
    #     return False

    column_list = ['id', 'name', 'questions']
    column_searchable_list = ['id', 'name']
    column_filters = ("id", 'name', 'questions')

    form_edit_rules = [
        'name',
    ]

    form_create_rules = [
        'name',
    ]
