from flask import jsonify


def js(message='', status_code=200, key='message'):
	"""create json answer with status_code"""
	return jsonify({key: message}), status_code


def succ_status(code):
	"""is successful http status code"""
	return 200 <= code < 300


def key_exists(data, key):
	"""useful when dealing with <null> or not found in JSON issue"""
	try:
		return True, data[key]
	except KeyError:
		return False, None
