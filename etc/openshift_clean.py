#!/usr/bin/python
"""
THIS SCRIPT CLEANS ALL DATA IN YOUR QUOKKA DB
RUN ONLY IN OPENSHIFT DEMO DEPLOY
OR AT YOUR OWN RISK!!!!
"""
from quokka import create_app
from quokka.core.models.content import Content
from quokka.core.models.config import Config
from quokka.core.models.channel import Channel
from quokka.modules.accounts.models import User

app = create_app()

Content.drop_collection()
User.drop_collection()
Config.drop_collection()
Channel.drop_collection()