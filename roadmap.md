Quokka Roadmap
==============

Core
====
* image upload in TinyMCE with support to cloud upload or local storage via API
* Media center (for images and files), thumbnail engine (like thumbor and others), video/audio manager/ flask-uploads
* ContentBox (a special content which is a bundle of other contents and can be listed/embedded)
* i18n
* Blueprints manager admin view (manage folder, package etc..)
* Change the way blueprints are loaded - use strict settings
* Better settings management (maybe using drgarcia1986/simple-settings, create a flask-simple-settings)
* Create quokka-admin tool
* PIP package installs quokka-admin tool which only has commands to manage themes, modules and downloads quokka
* Upgrade to new version of Flask-Admin and find a better way to manage themes and custom static files (or replace flask-admin with ng-admin)
* Support to ipynb files upload and conversion before publish
* Search Component (configurable using mongo or E.S)
* API REST
* Simple form of posting static Page
* QuickPost content and Widget
* Better dashboard for index on admin with drag and drop changeable widgets
* include docs for "uwsgi -s /tmp/uwsgi.sock -w quokka:app"
