[![Stories in Ready](http://badge.waffle.io/rochacbruno/quokka.png)](http://waffle.io/rochacbruno/quokka)  [![Build Status](https://drone.io/github.com/rochacbruno/quokka/status.png)](https://drone.io/github.com/rochacbruno/quokka/latest) [![Twitter](https://twitter.com/images/resources/twitter-bird-16x16.png)](http://twitter.com/quokkaproject) [@quokkaproject](http://twitter.com/quokkaproject "@quokkaproject on twitter")

Quokka project - Flask and MongoDB powered CMS
===============================================

![logo](/docs/logo.png)


Quokka is a flexible content management platform powered by Python, Flask and MongoDB.

Quokka provides a "full-stack" Flask application plus a bunch of selected extensions to provide all the needed CMS admin features and a flexible-easy way to extend the platform with **quokka-modules** built following the Flask **Blueprints** pattern.

Requirements
============
- Python 2.7
- Flask
- mongoengine
- Babel
- Flask-Cache
- Flask-DebugToolbar
- Flask-Gravatar
- Flask-HTMLBuilder
- Flask-Mail
- Flask-Script
- Flask-Security
- Flask-SuperAdmin
- Flask-Testing
- Flask-WTF
- Flask-Mongoengine


Installing and running
======================

#### On a *nix shell, do:

```bash
~/$ virtualenv quokka-env
~/$ ... creating virtualenv in quokka-env........
~/$ cd quokka-env
~/quokka-env$ source bin/activate
(quokka-env)~/quokka-env$ git clone https://github.com/rochacbruno/quokka
(quokka-env)~/quokka-env$ ...cloning in to quokka
(quokka-env)~/quokka-env$ cd quokka
(quokka-env)~/quokka-env/quokka$ pip install -r requirements.txt
```


#### configure your DATABASE settings

> Note: You need to have mongoDB installed on your server, optionally you can use mongolab.

```bash
(quokka-env)$ youreditor quokka/settings.py
######## YOUR EDITOR ################

MONGODB_SETTINGS = {'DB': "quokka_1"}


######################################
```

#### Test
```bash
(quokka-env)$ python runtests.py
...
----------------------------------------------------------------------
Ran 400 tests in 0.230s

OK

```

#### Create a super user
```bash
(quokka-env)$ python manage.py createsuperuser
Name: Input your name
Email: You@You.com
password: ***not1234***
```

#### Run
```bash
(quokka-env)$ python manage.py runserver
17.07 17:06:24 werkzeug     INFO      * Running on http://127.0.0.1:5000/
```

#### Enjoy!

- Sample home page: http://localhost:5000
- Admin interface http://localhost:5000/admin

Extending
==========

Quokka tries to implement the Django-ish way to implement **quokka-modules** it means that you can develop like this:

```bash
quokka/modules
│
└── posts
    ├── admin.py  - defines the admin pages
    ├── commands.py - create management commands here
    ├── __init__.py - define module and routes
    ├── models.py - define the Mongo Documents models
    ├── tasks.py - Tasks is for celery tasks
    ├── template_filters.py - Jinja filters
    ├── templates
    │   └── posts
    │       ├── detail.html
    │       └── list.html
    └── static
    └── views.py - module views
```


> **Important** - read more about developing modules in the docs, to avoid name conflicts your module should follow the naming pattern described in docs.

Installing modules
===================

**There is no need to install** or include your modules in config files or change quokka code to load the module.

Just drop your module package in **quokka/modules** restart your server and done!

Quokka admin also provides a web interface for admin-users to install and ENABLE/DISABLE modules.

Admin interface
================

Admin interface uses a customized version of Flask-SuperAdmin

![admin_overview](/docs/admin_overview.png)

Project tree
============
```bash
.
├── docs
│   ├── avatar.png
│   ├── logo.png
│   ├── _themes
│   │   ├── flask
│   │   │   ├── layout.html
│   │   │   ├── relations.html
│   │   │   ├── static
│   │   │   │   ├── flasky.css_t
│   │   │   │   └── small_flask.css
│   │   │   └── theme.conf
│   │   ├── flask_small
│   │   │   ├── layout.html
│   │   │   ├── static
│   │   │   │   └── flasky.css_t
│   │   │   └── theme.conf
│   │   ├── flask_theme_support.py
│   │   ├── LICENSE
│   │   └── README
│   └── tree.txt
├── LICENSE
├── Makefile
├── manage.py
├── MANIFEST.in
├── quokka
│   ├── bin
│   │   ├── __init__.py
│   │   └── quokka-admin.py
│   ├── contrib
│   │   └── __init__.py
│   ├── core
│   │   ├── admin
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── views.py
│   │   ├── basic_auth.py
│   │   ├── db.py
│   │   ├── __init__.py
│   │   ├── mail.py
│   │   ├── middleware.py
│   │   └── models.py
│   ├── ext
│   │   ├── babel.py
│   │   ├── before_request.py
│   │   ├── blueprints.py
│   │   ├── context_processors.py
│   │   ├── error_handlers.py
│   │   ├── generic.py
│   │   ├── __init__.py
│   │   ├── template_filters.py
│   │   └── views.py
│   ├── __init__.py
│   ├── local_settings.py
│   ├── media
│   │   ├── files
│   │   └── images
│   ├── modules
│   │   ├── accounts
│   │   │   ├── admin.py
│   │   │   ├── commands.py
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── __init__.py
│   │   └── posts
│   │       ├── admin.py
│   │       ├── commands.py
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── tasks.py
│   │       ├── template_filters.py
│   │       ├── templates
│   │       │   └── posts
│   │       │       ├── detail.html
│   │       │       └── list.html
│   │       └── views.py
│   ├── settings.py
│   ├── static
│   │   ├── admin
│   │   ├── css
│   │   ├── img
│   │   └── js
│   ├── templates
│   │   ├── admin
│   │   │   ├── denied.html
│   │   │   ├── index.html
│   │   │   └── layout.html
│   │   ├── base.html
│   │   └── _forms.html
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_basic.py
│   ├── test_settings.py
│   └── utils
│       ├── __init__.py
│       ├── settings.py
│       └── translation.py
├── README.md
├── README.rst
├── requirements.txt
├── roadmap.md
├── run.py
├── runtests.py
├── setup.py
└── wsgi.py

29 directories, 75 files
```

![python](/docs/python_powered.png)
![flask](/docs/flask_powered.png)
![mongo](/docs/mongo_powered.jpg)