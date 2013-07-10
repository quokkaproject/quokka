Quokka Roadmap
==============

Core
====
* auth module with generic switchable User model (http://pythonhosted.org/Flask-Security/)
* Media center (for images and files), thumbnail engine, video/audio manager/ flask-uploads
* Rich text Aloha editor widget
* core models for Site, Channels(MPTT), Categories, Tags, Slug, Published, Image, Config  etc...
* ContentBox
* Core generic views
* admin index view (customizable)
* i18n
* Blueprints manager admin view (manage folder, package etc..)
* Theming support (take a look at flask-themes)

Docs
===
- http://pythonhosted.org/Flask-Security/configuration.html
- from flask.ext.security import login_required, roles_required, roles_accepted

Blueprints (built_in)
=====================
* Post
* Comment
* Album
* Page
* Search
* API with flask-restful http://flask-restful.readthedocs.org/en/latest/

Blueprints (blueprint central)
==============================
* Poll
* Recipe
* Feedcrawler
* Social
* Ganalytics