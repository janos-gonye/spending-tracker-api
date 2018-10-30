from flask_mail import Mail


def init_app(app):
	mail.init_app(app)

mail = Mail()
