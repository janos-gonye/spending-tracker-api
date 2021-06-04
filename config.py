from os import environ

# Basic stuff
SECRET_KEY 						= environ.get('SECRET_KEY', 'secret_key_123')
DEBUG                           = int(environ.get('FLASK_DEBUG', 1))

# smtp and sending mails
MAIL_SERVER 					= environ.get('MAIL_SERVER')
MAIL_PORT 						= environ.get('MAIL_PORT')
MAIL_USE_TLS 					= int(environ.get('MAIL_USE_TLS', 1))
MAIL_USE_SSL 					= int(environ.get('MAIL_USE_SSL', 1))
MAIL_DEBUG 						= int(environ.get('MAIL_DEBUG', 1))
MAIL_USERNAME 					= environ.get('MAIL_USERNAME')
MAIL_PASSWORD 					= environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER 			= environ.get('MAIL_DEFAULT_SENDER')
MAIL_MAX_EMAILS 				= int(environ.get('MAIL_MAX_EMAILS'))
MAIL_ASCII_ATTACHMENTS 			= int(environ.get('MAIL_ASCII_ATTACHMENTS'))

# Database related
POSTGRES_HOST                       = environ.get('POSTGRES_HOST')
POSTGRES_USER                       = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD                   = environ.get('POSTGRES_PASSWORD')
POSTGRES_DB                         = environ.get('POSTGRES_DB')
POSTGRES_PORT                       = environ.get('POSTGRES_PORT')
SQLALCHEMY_DATABASE_URI             = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS 	    = int(environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 0))

# Non flask or flask extension related
REGISTRATION_TOKEN_LIFETIME 		= int(environ.get('REGISTRATION_TOKEN_LIFETIME', 24 * 60 * 60)) # seconds
CANCEL_REGISTRATION_TOKEN_LIFETIME	= int(environ.get('CANCEL_REGISTRATION_TOKEN_LIFETIME', 24 * 60 * 60)) # seconds
LOGIN_TOKEN_LIFETIME				= int(environ.get('LOGIN_TOKEN_LIFETIME', 60 * 60)) # seconds
RESET_PASSWORD_TOKEN_LIFETIME       = int(environ.get('RESET_PASSWORD_TOKEN_LIFETIME', 60 * 60)) # seconds
REFRESH_TOKEN_LIFETIME              = int(environ.get('REFRESH_TOKEN_LIFETIME', 30 * 24 * 60 * 60)) # seconds

# Password related
PASSWORD_MIN_LEN = int(environ.get('PASSWORD_MIN_LEN', 6))
PASSWORD_MAX_LEN = int(environ.get('PASSWORD_MAX_LEN', 50))

del environ
