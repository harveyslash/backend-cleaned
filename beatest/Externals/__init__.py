"""
Externals Package.

Meant for wrapping logic that involves calling 3rd party services like
Facebook,Google, RazorPay etc.

Any 3rd party api calls should be made from here

"""

from .BingSpellCheck import BingSpellCheck
from .CaaS import CaaS
from .Discourse import Discourse
from .FacebookOauth import FacebookOauth
from .Razorpay import Razorpay
from .ReCAPTCHA import ReCAPTCHA
