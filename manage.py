#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask.ext.script import Manager, Server
from flask.ext.collect import Collect
from quokka import create_app
from quokka.core.db import db
from quokka.ext.blueprints import load_blueprint_commands

app = create_app()

if app.config.get("LOGGER_ENABLED"):
    logging.basicConfig(
        level=getattr(logging, app.config.get("LOGGER_LEVEL", "DEBUG")),
        format=app.config.get(
            "LOGGER_FORMAT",
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'),
        datefmt=app.config.get("LOGGER_DATE_FORMAT", '%d.%m %H:%M:%S')
    )

manager = Manager(app)
manager.add_option("-c", "--config",
                   dest="config", required=False,
                   default='quokka.settings')

collect = Collect()
collect.init_script(manager)


@manager.shell
def make_shell_context():
    " Update shell. "
    return dict(app=app, db=db)


@manager.command
def check():
    """Prints app status"""
    from pprint import pprint
    print("Extensions.")
    pprint(app.extensions)
    print("Modules.")
    pprint(app.blueprints)
    print("App.")
    return app


@manager.command
def populate():
    """Populate the database with sample data"""
    from quokka.utils.populate import Populate
    Populate(db)()


@manager.command
def show_config():
    "print all config variables"
    from pprint import pprint
    print("Config.")
    pprint(dict(app.config))

manager.add_command("run0", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=8000
))

load_blueprint_commands(manager)

if __name__ == '__main__':
    manager.run()
