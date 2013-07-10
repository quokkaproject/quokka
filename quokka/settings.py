#coding: utf-8
import os

MONGODB_SETTINGS = {'DB': "quokka_1"}
SECRET_KEY = "KeepThisS3cr3t"

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
BLUEPRINTS_PATH = 'modules'
BLUEPRINTS_OBJECT_NAME = 'module'
SUPER_ADMIN = {'name': 'Quokka admin', 'url': '/admin'}

FILE_ADMIN = [
    {
        "name": "template_files",
        "category": "files",
        "path": os.path.join(PROJECT_ROOT, 'templates'),
        "url": "/template_files"
    },
    {
        "name": "static_files",
        "category": "files",
        "path": STATIC_ROOT,
        "url": "/static_files"
    },
    {
        "name": "media_files",
        "category": "files",
        "path": MEDIA_ROOT,
        "url": "/media_files"
    }
]

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

GRAVATAR = {
    'size': 100,
    'rating': 'g',
    'default': 'retro',
    'force_default': False,
    'force_lower': False
}

# http://pythonhosted.org/Flask-Mail/
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
# MAIL_USE_SSL = True
MAIL_USE_TLS = True
MAIL_USERNAME = 'rochacbruno@gmail.com'
# Create a email_password.txt in a safe location
MAIL_PASSWORD = open('/home/rochacbruno/email_password.txt').read()

# http://pythonhosted.org/Flask-Security/configuration.html
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_URL_PREFIX = '/accounts'
SECURITY_PASSWORD_SALT = '6e95b1ed-a8c3-4da0-8bac-6fcb11c39ab4'
SECURITY_EMAIL_SENDER = 'reply@localhost'
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True