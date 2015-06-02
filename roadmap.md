Quokka Roadmap
==============

Core
====
* image upload in TinyMCE with support to cloud upload or local storage via API
* Better tag widget in admin (using autocomplete for existing tags)
* Redirect content type (as link)
* Create a "NOTE" content type with minimum requirements
* Multiple language reference for contents using language slug prefix
* Create ARQUIVE template filter, displays a wordpress like arquive menu separating itens by year/month
* Create AUTHORS template filter to be used in bundles to show author names and links
* GROUP Settings in ADMIN for better visualization
* Finish cache implementation (redis as option)
* TITLE and TAGS management by content type and channel for better SEO
* Create a SIDEBAR widget (as default as a bundle content) to create a sidebar filled with links and a bundle manager to manage things like sidebar (needs to be generic ans can be used to create many bars in the site
* Create a command in admin to clone/copy a post
* In dashboard include a filter to see only DRAFTS (unpublished posts)
* Control visibility (by role) for posts also instead only by channels (currently suported)
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
* Implement a task queue, for sending email notifications, configurable to use python-rq or celery with https://github.com/Robpol86/Flask-Celery-Helper
* Adapt purepelican theme as default front end theme
* mkdocs in website
