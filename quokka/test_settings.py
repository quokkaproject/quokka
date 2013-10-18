#coding: utf-8

"""
This file is used for runtests.py or make test
"""

from quokka.settings import *

# MONGODB_SETTINGS = {'DB': "quokka_test"}  # use in localhost

MONGODB_SETTINGS = {'DB': 'quokka_local',
                    'USERNAME': 'quokka',
                    'PASSWORD': '302010'}

MODE = 'testing'
DEBUG = False
DEBUG_TOOLBAR_ENABLED = False
