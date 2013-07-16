#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager, Server
from flask.ext.collect import Collect
from quokka import create_app
from quokka.core.db import db
from quokka.tests import Test
from quokka.ext.blueprints import load_blueprint_commands

app = create_app()

manager = Manager(app)
manager.add_option("-c", "--config",
                   dest="config", required=False,
                   default='quokka.settings')

collect = Collect()
collect.init_script(manager)


manager.add_command("test", Test())


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
