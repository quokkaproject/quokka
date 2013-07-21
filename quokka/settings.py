#coding: utf-8
import os
import logging
#from quokka.utils.settings import get_password

MONGODB_SETTINGS = {'DB': "quokka_1"}  # use in localhost
# MONGODB_SETTINGS = {'DB': "quokka",
#                     'USERNAME': 'quokka',
#                     'PASSWORD': get_password('db'),
#                     'HOST': 'ds035498.mongolab.com',
#                     'PORT': 35498}  # use for mongolab

SECRET_KEY = "KeepThisS3cr3t"

CACHE_TYPE = "simple"

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
BLUEPRINTS_PATH = 'modules'
BLUEPRINTS_OBJECT_NAME = 'module'
SUPER_ADMIN = {'name': 'Quokka admin', 'url': '/admin'}

ADMIN_BRAND = """
<div class='brand'>
    <a href="/admin" title="Replace it with your logo in settings.ADMIN_BRAND">
        <img src='/static/img/logo.png' width='180' />
    </a>
</div>
<br>
""".strip()

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

COLLECT_STATIC_ROOT = STATIC_ROOT

MODE = 'production'
DEBUG = False

# Debug toolbar only works if installed
# pip install flask-debugtoolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_PROFILER_ENABLED = True
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
DEBUG_TB_PANELS = (
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask.ext.mongoengine.panels.MongoDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
)
DEBUG_TOOLBAR_ENABLED = False


GRAVATAR = {
    'size': 100,
    'rating': 'g',
    'default': 'retro',
    'force_default': False,
    'force_lower': False
}

# Emails go to shell until you configure this
# http://pythonhosted.org/Flask-Mail/
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# # MAIL_USE_SSL = True
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'rochacbruno@gmail.com'
# # Create a email_password.txt in a safe location
# MAIL_PASSWORD = get_password('email')

# DEFAULT_MAIL_SENDER = None

# http://pythonhosted.org/Flask-Security/configuration.html
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_URL_PREFIX = '/accounts'
SECURITY_PASSWORD_SALT = '6e95b1ed-a8c3-4da0-8bac-6fcb11c39ab4'
SECURITY_EMAIL_SENDER = 'reply@localhost'
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True


DEALER_PARAMS = dict(
    backends=('git', 'mercurial', 'simple', 'null')
)


# Babel
BABEL_LANGUAGES = ['en', 'pt-br']
BABEL_DEFAULT_LOCALE = 'en'


# WTForms
CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d.%m %H:%M:%S')
logging.info("Core settings loaded.")
