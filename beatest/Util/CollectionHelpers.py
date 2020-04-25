"""
Collection Helper module.

Has useful functions that are used for lists,dicts, or other collections
of objects.

"""


def get_attributes_dict(attr, arr):
    """
    A helper to pick out which dictionary to use from inside a list
    for the next serializer.

    :param attr: the attribute to search for
    :param arr: the array of attributes
    :return: if a dict with the key of attribute is found, the value of the key
            (which should be a list of attributes) is returned.
    """
    for elem in arr:
        if type(elem) is dict:
            if attr in elem:
                return elem[attr]
    return None
