from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

SECRET_KEY = environ.get('SECRET_KEY')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
MAIL_SERVER = environ.get('MAIL_SERVER')
MAIL_USERNAME = environ.get('MAIL_USERNAME')
MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_MAX_EMAIL = None
MAIL_ASCII_ATTACHMENT = False