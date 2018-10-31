from flask import jsonify


def js(message='', status_code=200):
	return jsonify({"message": message}), status_code
