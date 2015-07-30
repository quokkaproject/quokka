# coding: utf-8
import os

# MONGO
MONGODB_DB = os.environ['OPENSHIFT_APP_NAME']
MONGODB_HOST = os.environ['OPENSHIFT_MONGODB_DB_URL']
MONGODB_PORT = os.environ['OPENSHIFT_MONGODB_DB_PORT']
MONGODB_USERNAME = os.environ['OPENSHIFT_MONGODB_DB_USERNAME']
MONGODB_PASSWORD = os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']

# Logger
LOGGER_ENABLED = True
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%d.%m %H:%M:%S'

if os.environ['OPENSHIFT_APP_NAME'] == 'quokkadevelopment':
    DEBUG_TOOLBAR_ENABLED = True
    DEBUG = True

SHORTENER_ENABLED = True
