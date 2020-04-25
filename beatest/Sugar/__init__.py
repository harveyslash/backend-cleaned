"""
Syntactic Sugar package.
This package is designed to improve the features of
flask itself.

Most of the features are generic and unrelated to any
particular use case.
"""

__author__ = "Harshvardhan Gupta"
from .Auth import requires_roles
from .Cachify import cachify
from .Dictify import Dictifiable, ModelJSONEncoder
from .ErrorHandlers import setup_error_handlers
from .Flask import Flask
from .JSONifiedNestableBlueprint import JSONifiedNestableBlueprint
from .LoginManagerHandlers import setup_login_manager
from .ReqValDecorator import requires_validation

