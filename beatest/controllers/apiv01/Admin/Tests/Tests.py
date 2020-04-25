from Sugar import JSONifiedNestableBlueprint
from models import Test
from .Sections import admin_sections_controller

admin_tests_controller = JSONifiedNestableBlueprint("Admin Tests", __name__)
admin_tests_controller.register_blueprint(admin_sections_controller,
                                          url_prefix='/sections')


@admin_tests_controller.route('/tests', methods=['GET'])
def get_admin_tests():
    """
    List of existing Tests
    :return:
    """
    return Test.query.all()
