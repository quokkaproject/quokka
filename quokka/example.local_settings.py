# coding: utf-8

"""
Quokka will try to read configurations from environment variables
so you dont need this local_settings.py file if you have env vars.

1. You can set as a file

export QUOKKA_SETTINGS='/path/to/settings.py'

2. You can set individual values

export QUOKKA_MONGODB_DB="quokka_db"
export QUOKKA_MONGODB_HOST='localhost'
export QUOKKA_MONGODB_PORT='$int 27017'

Or just fill your values in this file and rename it to 'local_settings.py'
"""

# MONGO
MONGODB_DB = "quokka_db"
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None

# Debug and toolbar
DEBUG = True
DEBUG_TOOLBAR_ENABLED = False

# Logger
LOGGER_ENABLED = True
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%d.%m %H:%M:%S'

"""
If you want to have a new theme installed you can use quokkacms tool
    $ pip install quokkacms
    $ cd quokka
    $ quokkacms install_theme material
The above commands will download material design theme to your themes folder,
then just enable it.

DEFAULT_THEME = 'material'
"""
