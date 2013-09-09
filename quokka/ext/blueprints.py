# coding: utf-8
import os
import importlib
import random
import logging
from flask.ext.script import Command

logger = logging.getLogger()


def load_from_packages(app):
    pass


def load_from_folder(app):
    """
        This code looks for any modules or packages in the given
        directory, loads them
        and then registers a blueprint
        - blueprints must be created with the name 'module'
        Implemented directory scan

        Bulk of the code taken from:
            https://github.com/smartboyathome/
               Cheshire-Engine/blob/master/ScoringServer/utils.py
    """
    blueprints_path = app.config.get('BLUEPRINTS_PATH', 'modules')
    path = os.path.join(
        app.config.get('PROJECT_ROOT', '..'),
        blueprints_path
    )
    base_module_name = ".".join([app.name, blueprints_path])
    dir_list = os.listdir(path)
    mods = {}
    object_name = app.config.get('BLUEPRINTS_OBJECT_NAME', 'module')
    for fname in dir_list:
        if not os.path.exists(os.path.join(path, fname, 'DISABLED')) and  \
                os.path.isdir(os.path.join(path, fname)) and \
                os.path.exists(os.path.join(path, fname, '__init__.py')):

            # register blueprint object
            module_name = ".".join([base_module_name, fname])
            mods[fname] = importlib.import_module(module_name)
            blueprint = getattr(mods[fname], object_name)

            if not blueprint.name in app.blueprints:
                app.register_blueprint(blueprint)
            else:
                blueprint.name += str(random.getrandbits(8))
                app.register_blueprint(blueprint)
                logger.warning(
                    "CONFLICT:{0} already registered, using {1}".format(
                        fname, blueprint.name
                    )
                )

            # register admin
            try:
                importlib.import_module(".".join([module_name, 'admin']))
            except ImportError:
                logger.info(
                    "{0} module does not define admin".format(fname)
                )

    logger.info("{0} modules loaded".format(mods.keys()))


def load_blueprint_commands(manager):
    app = manager.app
    blueprints_path = app.config.get('BLUEPRINTS_PATH', 'modules')
    path = os.path.join(
        app.config.get('PROJECT_ROOT', '..'),
        blueprints_path
    )
    base_module_name = ".".join([app.name, blueprints_path])
    dir_list = os.listdir(path)
    mods = {}
    for fname in dir_list:
        if not os.path.exists(os.path.join(path, fname, 'DISABLED')) and  \
                os.path.isdir(os.path.join(path, fname)) and \
                os.path.exists(os.path.join(path, fname, '__init__.py')):

            # register management commands
            module_name = ".".join([base_module_name, fname])
            try:
                mod = importlib.import_module(
                    ".".join([module_name, 'commands'])
                )
                mods[fname] = mod
                for obj_name in dir(mod):
                    obj = getattr(mod, obj_name)
                    if obj_name != 'Command' and type(obj) == type and \
                            issubclass(obj, Command):
                        name = getattr(obj, 'command_name', obj_name.lower())
                        if name in manager._commands:
                            name += str(random.getrandbits(8))
                            logger.info("registering command {0}".format(name))
                        manager.add_command(name, obj())
            except ImportError:
                logger.info(
                    "{0} module does not define commands".format(fname)
                )
    logger.info("{0} management commands loaded".format(mods.keys()))
