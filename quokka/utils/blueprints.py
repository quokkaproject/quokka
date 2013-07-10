# coding: utf-8
import os
import imp


def load_blueprints_from_packages(app):
    pass


def load_blueprints_from_folder(app):
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

    path = os.path.join(
        app.config.get('PROJECT_ROOT', '..'),
        app.config.get('BLUEPRINTS_PATH', 'blueprints')
    )

    dir_list = os.listdir(path)
    mods = {}

    object_name = app.config.get('BLUEPRINTS_OBJECT_NAME', 'module')

    for fname in dir_list:
        if not os.path.exists(os.path.join(path, fname, 'DISABLED')) and  \
                os.path.isdir(os.path.join(path, fname)) and \
                os.path.exists(os.path.join(path, fname, '__init__.py')):

            f, filename, descr = imp.find_module(fname, [path])
            mods[fname] = imp.load_module(fname, f, filename, descr)
            app.register_blueprint(getattr(mods[fname], object_name))

            # register admin
            if os.path.exists(os.path.join(path, fname, 'admin.py')):

                f, filename, descr = imp.find_module(
                    'admin',
                    [os.path.join(path, fname)]
                )

                # by loading the module the admin.register is executed
                imp.load_module(fname, f, filename, descr)

        elif os.path.isfile(os.path.join(path, fname)):

            name, ext = os.path.splitext(fname)
            if ext == '.py' and not name == '__init__':
                f, filename, descr = imp.find_module(name, [path])
                mods[fname] = imp.load_module(name, f, filename, descr)
                app.register_blueprint(getattr(mods[fname], object_name))
