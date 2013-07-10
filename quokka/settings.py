#coding: utf-8
import os

MONGODB_SETTINGS = {'DB': "quokka_1"}
SECRET_KEY = "KeepThisS3cr3t"

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
BLUEPRINTS_PATH = 'blueprints'
BLUEPRINTS_OBJECT_NAME = 'module'
SUPER_ADMIN = {'name': 'Quokka admin', 'url': '/admin'}

DEBUG = True
