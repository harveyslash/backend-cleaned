from os import path

from .Mail import Mail

templates_path = path.join(path.dirname(__file__), 'templates/')

# Define the Paths to the Email Templates Here #
WELCOME_MAIL = path.join(templates_path, 'welcome_mail')
SIGNUP_ACTIVATION = path.join(templates_path, 'signup_activation')
FORGOT_PASSWORD = path.join(templates_path, 'forgot_password')
INVOICE = path.join(templates_path, 'invoice')
CONTACT_US = path.join(templates_path, 'contact_us')
