from flask import jsonify


def js(message='', status_code=200):
	"""create json answer with status_code"""
	return jsonify({"message": message}), status_code


def succ_status(code):
	"""is successful http status code"""
	return 200 <= code < 300
