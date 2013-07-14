Quokka Roadmap
==============

Todo
====
Change every __import__ with importlib http://docs.python.org/2.7/library/importlib.html

Core
====
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
* Accounts
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

Notes
=====
http://majorz.github.io/flask-htmlbuilder/
https://github.com/playpauseandstop/Flask-Dropbox
http://pythonhosted.org/Flask-Social/
https://github.com/mattupstate/flask-social
https://github.com/mattupstate/flask-security
https://github.com/sashka/flask-googleauth
https://github.com/eugenkiss/Simblin
https://github.com/elasticsales/Flask-gzip
https://github.com/rahulkmr/flask-bigapp-template
https://github.com/dcolish/flask-markdown
https://github.com/zzzsochi/Flask-Gravatar
https://github.com/mattupstate/flask-rq
https://github.com/kazoup/flask-elasticsearch


/home/rochacbruno/tumblelog/bin/uwsgi -s /tmp/uwsgi.sock -w quokka:app

https://flask-mongoengine.readthedocs.org/en/latest/