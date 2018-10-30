import re


EMAIL_REGEX = r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'



def validate_password(password):
	valid = True

	if len(password) < 6 or len(password) > 50 or \
	   not re.search(r"[a-z]", password) or \
	   not re.search(r"[A-Z]", password) or \
	   not re.search(r"[0-9]", password):
		valid = False
	return valid


def validate_email(email):
	return bool(re.match(EMAIL_REGEX, email))
