from os import environ


DEBUG = environ.get('DEBUG') == 'True'
ENV = environ.get('ENV')
SECRET_KEY = environ.get('SECRET_KEY')

# del environ
