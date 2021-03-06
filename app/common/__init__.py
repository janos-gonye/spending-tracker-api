from datetime import datetime, timezone
from re import compile

from flask import current_app as app
from flask import jsonify, url_for


def js(message='', status_code=200, key='message', **kwargs):
    """create json answer with status_code"""
    # Be careful, only 'if message' is not enough, becase a message can
    # be a boolean or interable value, too.
    if message is not None:
        json = {key: message}
    else:
        json = {}
    for key_, item in kwargs.items():
        assert key_ != key
        json[key_] = item
    return jsonify(json), status_code


def succ_status(code):
    """is successful http status code"""
    return 200 <= code < 300


def key_exists(data, key):
    """useful when dealing with <null> or not found in JSON issue"""
    try:
        return True, data[key]
    except KeyError:
        return False, None


def is_utc(string):
    re = compile(r"^([\+-]?\d{4}(?!\d{2}\b))((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d|[12]\d{2}|3([0-5]\d|6[1-6])))([T\s]((([01]\d|2[0-3])((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?$")
    return bool(re.search(string))


def datetime2timestamp(date):
    return date.replace(tzinfo=timezone.utc).timestamp()


def timestamp2datetime(timestamp):
    return datetime.utcfromtimestamp(float(timestamp))


def is_timestamp(string):
    try:
        if 0 > float(string):
            raise ValueError
        return True
    except ValueError:
        return False


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def create_link(url_root, endpoint, token=None):
    # Always send link with https in production
    if not app.config['DEBUG'] and not url_root.startswith('https'):
        url_root = url_root.replace('http', 'https')
    # Remove the first '/' character
    link = url_root + url_for(endpoint)[1:]
    if token:
        link = link + f"?token={token}"
    return link
