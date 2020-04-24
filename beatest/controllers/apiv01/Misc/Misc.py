from flask import request

from Mail import CONTACT_US, Mail
from Sugar import JSONifiedNestableBlueprint, requires_validation
from .req_val import ContactUsInputs

misc_controller = JSONifiedNestableBlueprint('Misc', __name__)


@misc_controller.route("/misc/contact_us", methods=['Post'])
@requires_validation(ContactUsInputs)
def contact_us():
    """
    Receives query message and sends it to the email in the request,
    and also "hello@beatest.in"

    """
    req = request.json
    del req['captcha_token']
    email = req['email']

    Mail([email, 'contact@beatest.in', 'sayantan@beatest.in'],
         req, req, req, CONTACT_US).send()
