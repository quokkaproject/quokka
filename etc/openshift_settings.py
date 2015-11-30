# coding: utf-8
import os

# MONGO
MONGODB_DB = os.environ['OPENSHIFT_APP_NAME']
MONGODB_HOST = os.environ['OPENSHIFT_MONGODB_DB_HOST']
MONGODB_PORT = int(os.environ['OPENSHIFT_MONGODB_DB_PORT'])
MONGODB_USERNAME = os.environ['OPENSHIFT_MONGODB_DB_USERNAME']
MONGODB_PASSWORD = os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']

SECURITY_REGISTERABLE = False
SECURITY_CHANGEABLE = False
SECURITY_RECOVERABLE = False

ADMIN_VIEW_EXCLUDE = [
    'quokka.modules.accounts.models.User',
    'quokka.modules.accounts.models.Role',
    'quokka.modules.accounts.models.Connection'
]

# Logger
LOGGER_ENABLED = True
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%d.%m %H:%M:%S'

if os.environ['OPENSHIFT_APP_NAME'] == 'quokkadevelopment':
    DEBUG_TOOLBAR_ENABLED = True
    DEBUG = True

SHORTENER_ENABLED = True
# SERVER_NAME = os.environ['OPENSHIFT_APP_DNS']

MAP_STATIC_ROOT = (
    '/robots.txt',
    '/sitemap.xml',
    '/favicon.ico',
    '/vaddy-c603c78bbeba8d9.html'
)

ADMIN_HEADER = (
    "<ul>"
    "<li class='alert'>User management is disabled in demo mode!</li>"
    "<li class='alert'>Demo server is limited, so it can be slow :(</li>"
    "<li class='alert'>"
    "<a href='https://quokkaslack.herokuapp.com/'>"
    "<img src='https://camo.githubusercontent.com/4a26f42037d8f75f8826561de4"
    "c0ad2ae8ac2701/68747470733a2f2f696d672e736869656c64732e696f2f6261646765"
    "2f4a4f494e5f534c41434b2d434841542d677265656e2e737667' "
    "alt='Join Slack Chat'></a>"
    "</li>"
    "</ul>"
)
