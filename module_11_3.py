import inspect
from inspect import ismethod
from inspect import isfunction
from inspect import getmembers
from inspect import getmodule
from pprint import pprint


def introspection_info(obj):
    obj_info = {}
    try:
        obj_info['type'] = type(obj)
        obj_info['module'] = getmodule(obj)
        obj_info['attributes'] = [m[0] for m in getmembers(obj)]
        obj_info['functions'] = [attr[0] for attr in getmembers(obj) if isfunction]
        obj_info['methods'] = [m[0] for m in getmembers(obj) if ismethod]
        obj_info['not_sys_attributes'] = [m[0] for m in getmembers(obj) if not m[0].startswith('__')]
        obj_info['callable_attributes'] = [m[0] for m in inspect.getmembers(obj, predicate=callable)]
        obj_info["name"] = obj.__name__
    except AttributeError as err_attr:
        print(f"AttributeError: {err_attr}")
    return obj_info

try:
    obj = 42
    result = introspection_info(obj)
    pprint(result)
except NameError as n_err:
    print(f"NameError: {n_err} \nPlease enter a valid name")
