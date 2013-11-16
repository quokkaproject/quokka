#coding: utf-8
import os

"""
the get_password function tries to find a file called
<arg>_password.txt containing the txt.

By default it looks in application root folder parent.

get_password('db') - > ../db_password.txt

Import it if you want to pass some password to your configs.
"""
# from quokka.utils.settings import get_password


"""
DB for localhost
"""
MONGODB_SETTINGS = {'DB': "quokka_db"}

"""
DB in remote host
- register for free in mongolab.com
"""
# MONGODB_SETTINGS = {'DB': "quokka",
#                     'USERNAME': 'quokka',
#                     'PASSWORD': get_password('db'),
#                     'HOST': 'ds035498.mongolab.com',
#                     'PORT': 35498}

"""
This should really be secret for security
use os.random, urandom or uuid4 to generate
in your shell
$ python -c "import uuid;print uuid.uuid4()"
then use the generated key
"""
SECRET_KEY = "KeepThisS3cr3t"

"""
Take a look at Flask-Cache documentation
"""
CACHE_TYPE = "simple"


"""
Not needed by flask, but those root folders are used
by FLask-Admin file manager
"""
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'mediafiles')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

"""
Files on MAP_STATIC_ROOT will be served from /static/
example: /static/favicon.ico will be served by site.com/favicon.ico
"""
MAP_STATIC_ROOT = ('/robots.txt', '/sitemap.xml', '/favicon.ico')


"""
If enabled admin will leave creation of repeated slugs
but will append a random int i.e: blog-post-2342342
"""
SMART_SLUG_ENABLED = False

"""
Blueprints are quokka-modules, you don't need to install
just develop or download and drop in your modules folder
by default it is in /modules, you can change if needed
"""
BLUEPRINTS_PATH = 'modules'
BLUEPRINTS_OBJECT_NAME = 'module'

"""
Default configuration for FLask-Admin instance
:name: - will be the page title
:url: - is the ending point
"""
ADMIN = {'name': 'Quokka admin', 'url': '/admin'}

"""
File admin can expose folders, you just need to have them
mapped in your server or in flask, see quooka.ext.views
"""
FILE_ADMIN = [
    {
        "name": "Template files",
        "category": "files",
        "path": os.path.join(PROJECT_ROOT, 'templates'),
        "url": "/template_files/",  # create nginx rule
        "endpoint": "template_files",
        "roles_accepted": ("admin", "editor")
    },
    {
        "name": "Static files",
        "category": "files",
        "path": STATIC_ROOT,
        "url": "/static/",  # create nginx rule
        "endpoint": "static_files",
        "roles_accepted": ("admin", "editor")
    },
    {
        "name": "Media files",
        "category": "files",
        "path": MEDIA_ROOT,
        "url": "/mediafiles/",  # Create nginx rule
        "endpoint": "media_files",
        "roles_accepted": ("admin", "editor")
    }
]

"""
This is for Flask-Collect extension
you can install blueprints with static files and run
python manage.py collectstatic to copy to main static folder
"""
COLLECT_STATIC_ROOT = STATIC_ROOT

"""
Never change it here, use local_settings for this.
"""
MODE = 'production'
DEBUG = False

"""
Debug toolbar only works if installed
pip install flask-debugtoolbar
"""
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_PROFILER_ENABLED = True
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
DEBUG_TB_PANELS = (
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    #'flask.ext.mongoengine.panels.MongoDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
)

"""
By default DEBUG_TOOLBAR is disabled
do not change it here, do it in local_settings.py
DEBUG_TOOLBAR_ENABLED = True
"""
DEBUG_TOOLBAR_ENABLED = False


"""
Flask-Gravatar can take avatar urls in jinja templates
do: {{ current_user.email | gravatar }} or
{{ 'some@server.com' | gravatar(size=50) }}
"""
GRAVATAR = {
    'size': 100,
    'rating': 'g',
    'default': 'retro',
    'force_default': False,
    'force_lower': False
}

"""
Emails go to shell until you configure this
http://pythonhosted.org/Flask-Mail/

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
# MAIL_USE_SSL = True
MAIL_USE_TLS = True
MAIL_USERNAME = 'rochacbruno@gmail.com'
# Create a .email_password.txt in ../
MAIL_PASSWORD = get_password('email')
DEFAULT_MAIL_SENDER = None
"""

"""
Take a look at Flask-Security docs
http://pythonhosted.org/Flask-Security/configuration.html
"""
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_URL_PREFIX = '/accounts'
SECURITY_PASSWORD_SALT = '6e95b1ed-a8c3-4da0-8bac-6fcb11c39ab4'
SECURITY_EMAIL_SENDER = 'reply@localhost'
SECURITY_REGISTERABLE = True
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True

SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_LOGIN_WITHOUT_CONFIRMATION = True

"""
Dealer can versionate static files if you are under a repo
in most cases you dont need to change this config
in templates you can do
<script src="{{ url_for('static', filename='xxx.js')}}?version={{revision}}" >
:revision: is the latest commit in the repository for this file.
"""
DEALER_PARAMS = dict(
    backends=('git', 'mercurial', 'simple', 'null')
)


"""
Internationalization for Flask-Admin
if want to use in your site home page, read babel docs.
"""
BABEL_LANGUAGES = ['en', 'pt-br']
BABEL_DEFAULT_LOCALE = 'en'


# WTForms
CSRF_ENABLED = True
"""
It is good to use uuid here
$ python -c "import uuid;print uuid.uuid4()"
"""
CSRF_SESSION_KEY = "somethingimpossibletoguess"


# configure logger in your local_settings
LOGGER_ENABLED = False
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%d.%m %H:%M:%S'

# media module
MEDIA_IMAGE_ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'tiff', 'gif', 'bmp')
MEDIA_AUDIO_ALLOWED_EXTENSIONS = ('mp3', 'wmv', 'ogg')
MEDIA_VIDEO_ALLOWED_EXTENSIONS = ('avi', 'mp4', 'mpeg')
MEDIA_FILE_ALLOWED_EXTENSIONS = ('pdf', 'txt', 'doc', 'docx', 'xls', 'xmlsx')

# default admin THEME
ADMIN_THEME = 'cosmo'

# default content extension for url buildind
CONTENT_EXTENSION = "html"
