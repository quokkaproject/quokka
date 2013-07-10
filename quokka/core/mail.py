# coding: utf-8
from flask.ext.mail import Mail, Message
from quokka import app

mail = Mail(app)


def send_mail(*args, **kwargs):
    msg = Message(*args, **kwargs)
    mail.send(msg)


def test():
    send_mail(
        "Hello",
        sender="rochacbruno@gmail.com",
        recipients=['rochacbruno@gmail.com'],
        body="Hello I am testing"
    )
