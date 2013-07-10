#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from utils.blueprints import load_blueprints_from_packages
from utils.blueprints import load_blueprints_from_folder


def create_app(config_filename='settings'):
    app = Flask(__name__)
    app.config.from_object('settings')
    load_blueprints_from_packages(app)
    load_blueprints_from_folder(app)
    return app
