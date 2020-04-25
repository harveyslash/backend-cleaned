"""
Dictify module.

A module to serialise database models based on attributes.
"""
import enum
import json
from datetime import datetime

from flask.json import JSONEncoder
from sqlalchemy import inspect

from Util.CollectionHelpers import get_attributes_dict
import decimal


class Dictifiable:
    """
    Dictifyable Class to automatically convert models to dict.
    Models should inherit this class to allow for serializing capabilities

    """

    def todict(self, attributes=None):

        if attributes is not None:
            return dictify(self, attributes)

        if hasattr(self, '_default_props'):
            return dictify(self, self._default_props)

        return dictify(self, attributes)

    def __repr__(self):
        dumps = json.dumps(self.todict(), sort_keys=True, indent=4)
        return f"{type(self).__name__}({dumps})"


def dictify(obj, attributes=None):
    """
    A function to parse model attributes and convert to native python objects.
    This is required so that jsonify can parse the results.
    This supports unlimited nesting.

    If attributes is none, this function looks for _default_props member
    in the class. If _default_props doesnt exist, then only the already loaded
    keys are returned. This prevents implicit db calls to the database.

    :param obj: the model object
    :param attributes: a list of attributes to parse for. it should contain
                        the names of the column names of the fields.
                        in case of a nested field, an additional dict
                        specifying the nested attributes should be present.
    :return: a serialised object that jsonify can understand
    """

    column_keys = inspect(type(obj)).columns.keys()
    relationship_keys = inspect(type(obj)).relationships.keys()

    try:
        if attributes is None:  # custom attributes were not supplied
            attributes = obj._default_props  # try _default props

    except AttributeError:
        # _default props doesnt exist
        # get all the loaded keys.
        attributes = column_keys + relationship_keys
        attributes = [attribute for attribute in attributes if attribute not
                                                               in inspect(
                obj).unloaded]

    result = {}
    # simple keys , like int, str, boolean
    simple_attrs = [x for x in column_keys if x in attributes]

    # relationship keys, which have references to other objects
    complex_attrs = [x for x in relationship_keys if x in attributes]

    for attribute in simple_attrs:

        attr_val = getattr(obj, attribute)

        # special handling for enum types
        if issubclass(type(attr_val), enum.Enum):
            result[attribute] = attr_val.name
            continue

        # special handling for date types
        if type(attr_val) is datetime:
            result[attribute] = attr_val.isoformat()
            continue

        # special handling for decimal types
        if type(attr_val) is decimal.Decimal:
            result[attribute] = float(attr_val)
            continue

        # if none of the cases match, just put the value directly
        result[attribute] = attr_val

    for attribute in complex_attrs:

        attr_val = getattr(obj, attribute)

        # if there is a one to many relationship
        if obj._sa_class_manager[attribute].property.uselist:

            # call the todict method of the related objects, and
            # attach to result as a list
            result[attribute] = [getattr(x, 'todict')(get_attributes_dict(
                    attribute, attributes)) for x in attr_val]
        else:  # if there is only one object to connect to

            # if the object is None, set None, else put the value
            result[attribute] = getattr(attr_val, 'todict')(
                    get_attributes_dict(
                            attribute,
                            attributes)) if attr_val is not None else None

    return result


class ModelJSONEncoder(JSONEncoder):
    """
    Class to encode sqlalchemy results to json.
    It is just a helper that calls the 'todict' method of the model.

    Any class that inherits Dictifyable has todict.

    """

    def default(self, obj):
        if hasattr(obj, 'todict'):
            return obj.todict()

        return JSONEncoder.default(self, obj)
