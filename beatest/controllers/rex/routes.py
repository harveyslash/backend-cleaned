from Sugar import JSONifiedNestableBlueprint
from .Users import rex_user_controller
from .TestAttempts import rex_testattempts_controller

base_blueprint = JSONifiedNestableBlueprint("REXBASE", __name__)

base_blueprint.register_blueprint(rex_user_controller)
base_blueprint.register_blueprint(rex_testattempts_controller)


@base_blueprint.route('', methods=['Post', 'Get'])
def echo_time():
    pass
