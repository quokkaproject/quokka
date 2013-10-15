# coding: utf-8
"""
DELETE THIS FILE IN PRODUCTION!!!!
"""

# from quokka.utils.settings import get_password

# MONGODB_SETTINGS = {'DB': "quokka",
#                     'USERNAME': 'quokka',
#                     'PASSWORD': get_password('db'),
#                     'HOST': 'ds035498.mongolab.com',
#                     'PORT': 35498}  # use for mongolab

MONGODB_SETTINGS = {'DB': 'local_test3'}
DEBUG = True
DEBUG_TOOLBAR_ENABLED = False

# configure logger in your local_settings
LOGGER_ENABLED = True
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%d.%m %H:%M:%S'
