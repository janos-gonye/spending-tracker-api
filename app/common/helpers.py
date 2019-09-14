from flask import current_app as app

from password_generator import PasswordGenerator


def generate_password():
    pwo = PasswordGenerator()
    pwo.minlen = app.config['PASSWORD_MIN_LEN']
    pwo.maxlen = app.config['PASSWORD_MAX_LEN']
    pwo.minschars = 0
    return pwo.generate()
