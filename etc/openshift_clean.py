#!/usr/bin/python
"""
THIS SCRIPT CLEANS ALL DATA IN YOUR QUOKKA DB
RUN ONLY IN OPENSHIFT DEMO DEPLOY
OR AT YOUR OWN RISK!!!!
"""
from quokka import create_app
from quokka.core.models import Content, Channel, Config
from quokka.modules.accounts.models import User

app = create_app()

Content.objects.delete()
User.objects.delete()
Config.objects.delete()

for channel in Channel.objects.filter(parent__ne=None):
    channel.delete()

Channel.objects.delete()
