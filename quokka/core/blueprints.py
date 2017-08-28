# coding: utf-8
import importlib
import os

from quokka.core.commands_collector import CommandsCollector


# def load_from_packages(app):
#     pass


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
    module_file = app.config.get('BLUEPRINTS_MODULE_NAME', 'main')
    blueprint_module = module_file + '.py'
    for fname in dir_list:
        if not os.path.exists(os.path.join(path, fname, 'DISABLED')) and  \
                os.path.isdir(os.path.join(path, fname)) and \
                os.path.exists(os.path.join(path, fname, blueprint_module)):

            # register blueprint object
            module_root = ".".join([base_module_name, fname])
            module_name = ".".join([module_root, module_file])
            mods[fname] = importlib.import_module(module_name)
            blueprint = getattr(mods[fname], object_name)
            app.logger.info("registering blueprint: %s" % blueprint.name)
            app.register_blueprint(blueprint)

            # register admin
            try:
                importlib.import_module(".".join([module_root, 'admin']))
            except ImportError as e:
                app.logger.info(
                    "%s module does not define admin or error: %s", fname, e
                )

    app.logger.info("%s modules loaded", mods.keys())


def get_blueprint_commands(path, root, app_name):
    modules_path = os.path.join(root, path)
    base_module_name = ".".join([app_name, path])
    cmds = CommandsCollector(modules_path, base_module_name)
    return cmds


def blueprint_commands(app=None):
    return get_blueprint_commands(
        path=app.config.get('BLUEPRINTS_PATH', 'modules'),
        root=app.config.get('PROJECT_ROOT', '..'),
        app_name=app.name
    )
