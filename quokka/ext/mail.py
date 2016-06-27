# coding: utf-8
from flask_mail import Mail

mail = Mail()


def configure(app):
    mail.init_app(app)
