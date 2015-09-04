# coding: utf-8
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
MONGODB_DB = "quokka_db"
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None

"""
This should really be secret for security
use os.random, urandom or uuid4 to generate
in your shell
$ python -c "import uuid;print uuid.uuid4()"
then use the generated key
"""
SECRET_KEY = "S3cr3Tk3Y"  # noqa

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
ROOT_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, '..'))

# For starting with sample data
POPULATE_FILEPATH = os.path.join(
    ROOT_DIR, 'etc', 'fixtures', 'initial_data.json'
)

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

DEFAULT_EDITABLE_EXTENSIONS = (
    'html', 'css', 'js', 'py', 'txt', 'md', 'cfg', 'coffee', 'html', 'json',
    'xml', 'yaml', 'yml', 'HTML', 'CSS', 'JS', 'PY', 'TXT', 'MD', 'CFG',
    'COFFEE', 'HTML', 'JSON', 'XML', 'YAML', 'YML'
)

FILE_ADMIN = [
    {
        "name": "Template files",
        "category": "Files",
        "path": os.path.join(PROJECT_ROOT, 'templates'),
        "url": "/template_files/",  # create nginx rule
        "endpoint": "template_files",
        "roles_accepted": ("admin", "editor"),
        "editable_extensions": DEFAULT_EDITABLE_EXTENSIONS
    },
    {
        "name": "Static files",
        "category": "Files",
        "path": STATIC_ROOT,
        "url": "/static/",  # create nginx rule
        "endpoint": "static_files",
        "roles_accepted": ("admin", "editor"),
        "editable_extensions": DEFAULT_EDITABLE_EXTENSIONS
    },
    {
        "name": "Media files",
        "category": "Files",
        "path": MEDIA_ROOT,
        "url": "/mediafiles/",  # Create nginx rule
        "endpoint": "media_files",
        "roles_accepted": ("admin", "editor"),
        "editable_extensions": DEFAULT_EDITABLE_EXTENSIONS
    }
]

"""
Activates Flask-Weasyprint extension
so that Posts can be rendered to PDF just by
changing the extension from .html to .pdf
please install Flask-Weasyprint in your python env
pip install flask-weasyprint
"""
ENABLE_TO_PDF = False

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
    'flask.ext.mongoengine.panels.MongoDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
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
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'  # noqa
SECURITY_URL_PREFIX = '/accounts'
SECURITY_PASSWORD_SALT = '6e95b1ed-a8c3-4da0-8bac-6fcb11c39ab4'  # noqa
SECURITY_EMAIL_SENDER = 'reply@localhost'
SECURITY_REGISTERABLE = False
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True

# Configurations below should be changes in local_settings
# when email system got setted up
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False

"Recaptcha for user register form"
SECURITY_RECAPTCHA_ENABLED = False
# RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
# RECAPTCHA_PUBLIC_KEY = ''
# RECAPTCHA_PRIVATE_KEY = ''

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
ADMIN_THEME = 'admin'
"""
https://bootswatch.com/2/ themes available:
amelia cerulean cosmo cyborg default flatly
journal readable simplex slate spacelab
spruce superhero united
"""
ADMIN_SWATCH = 'default'

ADMIN_ICONS = [
    ('post.create_view', 'pencil', 'Write'),
    ('post.index_view', 'th-list', 'Posts'),
    ('config.index_view', 'cog', 'Config'),
    ('user.index_view', 'user', 'Users'),
    ('image.index_view', 'picture', 'Images'),
    ('image.create_view', 'arrow-up', 'Upload'),
    ('channel.index_view', 'th-list', 'Channels')
]

# front end theme
DEFAULT_THEME = 'pure'

# default content extension for url buildind
CONTENT_EXTENSION = "html"

SENTRY_ENABLED = False
SENTRY_DSN = ""

# html or markdown
DEFAULT_TEXT_FORMAT = "html"

"Shortner urls configuration"
SHORTENER_ENABLED = False

"Note: if you enable shortener you have to define a SERVER_NAME"
# SERVER_NAME = 'localhost'

"Config shorter information"
SHORTENER_SETTINGS = {"name": "BitlyShortener",
                      "bitly_api_key": "R_7d84f09c68be4c749cac2a56ace2e73f",
                      "bitly_token":
                      "9964d1f9c8c8b4215f7690449f0980c4fe1a6906",
                      "bitly_login": "quokkabitly"}
