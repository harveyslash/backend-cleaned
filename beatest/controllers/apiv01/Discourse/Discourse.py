from flask import current_app, request
from flask_login import current_user, login_required

from Externals import Discourse
from Sugar import JSONifiedNestableBlueprint
from models import Error

discourse_blueprint = JSONifiedNestableBlueprint('Discourse', __name__)


@discourse_blueprint.route("/discourse_sso", methods=['POST'])
@login_required
def discourse_login():
    try:
        payload = request.args.get('sso')
        signature = request.args.get('sig')

        decoded = Discourse.parse_payload(payload, signature)
        query_string = Discourse.build_return_payload(decoded, current_user.id)

        url = f"{current_app.config['DISCOURSE_URL']}?{query_string}"
    except:
        return Error("Invalid query parameters provided", 403)()

    return {"url": url}
