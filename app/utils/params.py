from time import time

from flask import request


def _get_timestamp_param(name, default):
    param = request.args.get(name) or default
    param = str(param)
    if not param.isdigit():
        raise ValueError(f"Param {name} must be a natural number.")
    return int(param)


def get_param_from():
    return _get_timestamp_param(name='from', default=0)


def get_param_to():
    return _get_timestamp_param(name='to', default=int(time()))
