# coding: utf8
from flask import Blueprint
from flask.ext.security import Security, MongoEngineUserDatastore
from flask.ext.mail import Mail

from quokka import app
from quokka.core.db import db

mail = Mail(app)

from .models import Role, User

if not app.blueprints.get('security'):
    # Setup Flask-Security
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

module = Blueprint('accounts', __name__, template_folder='templates')
