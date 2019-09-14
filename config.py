from os import environ

# Basic stuff
DEBUG 							= environ.get('DEBUG') == 'True'
ENV 							= environ.get('ENV')
SECRET_KEY 						= environ.get('SECRET_KEY')
TESTING 						= environ.get('TESTING') == 'True'

# smtp and sending mails
MAIL_SERVER 					= environ.get('MAIL_SERVER')
MAIL_PORT 						= environ.get('MAIL_PORT')
MAIL_USE_TLS 					= environ.get('MAIL_USE_TLS') == 'True'
MAIL_USE_SSL 					= environ.get('MAIL_USE_SSL') == 'True'
MAIL_DEBUG 						= str(environ.get('MAIL_DEBUG', DEBUG)) == 'True'
MAIL_USERNAME 					= environ.get('MAIL_USERNAME')
MAIL_PASSWORD 					= environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER 			= environ.get('MAIL_DEFAULT_SENDER')
MAIL_MAX_EMAILS 				= environ.get('MAIL_MAX_EMAILS') if environ.get('MAIL_MAX_EMAILS') is None else int(environ.get('MAIL_MAX_EMAILS'))
MAIL_SUPPRESS_SEND 				= str(environ.get('MAIL_SUPPRESS_SEND', TESTING)) == 'True'
MAIL_ASCII_ATTACHMENTS 			= environ.get('MAIL_ASCII_ATTACHMENTS') == 'True'

# Database related
SQLALCHEMY_DATABASE_URI 		= environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS 	= environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'

# Non flask or flask extension related
REGISTRATION_TOKEN_LIFETIME 		= int(environ.get('REGISTRATION_TOKEN_LIFETIME', 24 * 60 * 60)) # seconds
CANCEL_REGISTRATION_TOKEN_LIFETIME	= int(environ.get('CANCEL_REGISTRATION_TOKEN_LIFETIME', 24 * 60 * 60)) # seconds
LOGIN_TOKEN_LIFETIME				= int(environ.get('LOGIN_TOKEN_LIFETIME', 60 * 60)) # seconds
CHANGE_PASSWORD_TOKEN_LIFETIME      = int(environ.get('CHANGE_PASSWORD_TOKEN_LIFETIME', 60 * 60)) # seconds

del environ
