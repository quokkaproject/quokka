#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Set the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from quokka import app

manager = Manager(app)

manager.add_command("runserser", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0'
))

if __name__ == '__main__':
    manager.run()
