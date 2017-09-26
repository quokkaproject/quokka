# Quokka CMS

![quokka](/docs/emoji_small.png)

## The Happiest CMS in the world

Quokka CMS is a Content Management System written in Python.

A lightweight framework to build websites, portals, blogs, applications
and anything related to publishing content to the web.

## Features

- Web based content management admin interface
- Multiple content formats (markdown, rst, html, plaintext)
- Compatibility with any of the [Pelican Themes](pelican-themes.org)
- Flat file NoSQL database **TinyDB** or optionally **MongoDB** for scale deployments
- Host the Quokka server or generate a static website
- Extensible via modules/plugins
- Powered by Python, Flask, Flask-Admin, TinyMongo and Pelican Themes

## Quick Start

### Install quokka

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install quokka
```

> NOTE: QuokkaCMS requires Python 3.6+

### Start a project

```bash

$ quokka init NewWebsite --theme=flex --modules=gitpages,heroku
...
```

```bash
🐹 Quokka project created 🐹
📝 Name: NewWebsite
📁 Location: /tmp/newwebsite
📚 Template: default
🎨 Themes: flex theme installed
🚚 Modules: [gitpages, heroku] installed
🔧 Config: Config file written in /tmp/newwebsite/quokka.yml
➡ Go to /tmp/newwebsite
⚙ run `quokka runserver` to start!
📄 Check the documentation on http://quokkaproject.org
🐹 Happy Quokka! 🐹
```

> YES! it outputs emojis 🐹


The above command will generate your project in `myproject` folder as:

```bash
.
├── databases        # TinyDB database files (gitignored)
├── modules          # Custom modules to load on EXTRA_EXTENSIONS
├── static_build     # output static site
├── themes           # Front-end Themes (Pelican and Quokka Themes supported)
├── uploads          # Media uploaded via admin
├── .gitignore       # gitignore to exclude sensitive files
├── quokka.yml       # Project settings
├── .secrets.yml     # To store keys, tokens and passwords (gitignored)
└── wsgi.py          # To deploy `gunicorn wsgi:app`
```

You can optionally pass arguments:

Choose existing theme (the default is [Malt](https://github.com/grupydf/malt))

```bash
quokka init mywebsite --theme http://github.com/user/theme
```

Install modules

```bash
quokka init mywebsite --theme http://github.com/user/theme --modules="commerce,foo"
```

> the above looks for `quokka_commerce` and `quokka_foo` in PyPI and installs it

Set important configurations

```bash
quokka init mywebsite --theme http://github.com/user/theme --config="auth_enabled=false"
```

> That is optional, you have to edit `quokka.yml` to tune your settings.

### Run your website

```bash
quokka runserver --port 5000
```

### Access admin interface

http://localhost:5000/admin

### Access your site

http://localhost:5000

## Deploy

### You can deploy your Quokka Website in a WSGI server

Check the `wsgi.py` and refer to it when deploying in wsgi servers.

```bash
cd myproject
gunicorn wsgi:app -w 4 -b "0.0.0.0:8000"
```

An example of `supervisord` config

```ini
[program:quokka]
command=/myproject/venv/bin/gunicorn wsgi:app -w 4 -b "0.0.0.0:8000"
directory=/myproject
```

For more information read [Gunicorn documentation](http://docs.gunicorn.org/en/stable/index.html)

## Publish Static HTML website

> **NOTE**: To generate a static website all user management, keys and passwords will be removed from settings.

### You can generate a static HTML website to host anywhere

Once you have your website running locally you can easily generate a
static HTML website from it.

```bash
$ quokka publish --static [--output path]
Generating static HTML website on ./static_build folder
```

Once you have a ./static_build folder populated with static website you can deploy it
using SCP, FTP or git, it is a full static website.

### Deploying to github pages from command line

> NOTE: You need either ssh key access to github or it will ask login/password

```bash
quokka publish --static --git=rochacbruno/mysite --branch=gh_pages
```

> The above is also available in admin under 'publish' menu.

### Deploying via SCP

```bash
quokka publish --static --scp --dest='me@hostname:/var/www/mysite' [--sshkey ~/.ssh/key] [--password xyz]
password : ...
```

### Deploying to Heroku

> This requires `heroku` client installed, if `Procfile` is not found it will be generated

```bash
quokka publish --static --heroku --options
```

### Deploying via FTP

```bash
quokka publish --static --ftp --host='ftp://server.com' --dest='/var/www/mysite'
```

### Load database from remote deployment (only for TinyDB)

When you publish a static website along with the static files the database also
goes to the server under the databases/ folder only as a backup and snapshot.

You can load that remote database locally e.g: to add new posts and then re-publish

```bash
quokka restoredb --remote --git=rochacbruno/mysite
Creating a backup of local database...
Downloading remote database
Restoring database..
Done...
```

Now you can run `quokka runserver` open your `localhost:5000/admin` write new content
and then `Publish` website again using command line or admin interface.

> NOTE: If you want to restore a local database use `--local` and `--path path/to/db`

## Using MongoDB

You can choose to use MongoDB instead of TinyDB, That is useful specially if
you deploy or local instance has more than one admin user concurrently
and also useful if you want to install plugins which support MongoDB only
(because it relies on aggregations and gridfs)

You only need a running instance
of Mongo server and change `quokka.yml:DB` on your project from:

```yaml
quokka:
  DB:
    system: tinydb
    folder: databases
```

to:

```yaml
quokka:
  DB:
    system: mongodb
    name: my_database
    host: 127.0.0.1
    port: 2600
```

Then when running `quokka` again it will try to connect to that Mongo Server.

With that you can deploy your site on `wsgi` server or can also generate `static` website.

### Running mongo in a Docker container

```bash
cd your_quokka_project_folder
docker run -d -v $PWD/databases:/data/db -p 27017:27017 mongo
# wait some seconds until mongo is started
quokka runserver
```

## Contributing to Quokka CMS Development

Do you want to be part of this open-source project?

Take a look at [Contributing Guidelines](/CONTRIBUTING.md)

## TODO

This is the list of tasks to be completed until `1.0.0` can be released.
support 100% coming only for malt and bootstrap3 themes

- [x] variable map (from content to theme)
- [x] list only categories with content in menu
- [x] handle spaces in category names/tagnames slugify?
- [ ] list only pages with 'show_in_menu' metadata on menu
- [ ] list only categories with 'show_in_menu' metadata on menu (will require metadata admin)
- [ ] sort options for menu
- [ ] optional footer elements on malt
- [ ] custom footer element by CONFIG_VAR (FOOTER_ELEMENTS:{1:'text'})
- [ ] create a EXCLUDE_FROM_MENU variable
- [ ] create a SHOW ONLY ROOT CATEGORIES ON MENU
- [ ] create a USE_CATEGORIES_DROPDOWN
- [ ] create a USE_PAGES_DROPDOWN
- [x] categories page
- [ ] tags/tag page
- [ ] authors/author page
- [ ] @author profile page (customizable)
- [ ] feeds
- [ ] sitemap
- [ ] search
- [ ] archives (date grouped content)
- [ ] Custom TinyDB serializators from modules
- [ ] admin config overrides
- [ ] split categories by `/` to get all roots
- [ ] content extra fields
- [ ] content custom metadata
- [ ] content translations
- [ ] content avatars
- [ ] content art/page comment attr
- [ ] date formatting from settings
- [ ] dynamic theme per category (deal cache..)
- [ ] implement pre-render and post-renders
- [ ] replacement marks [[x:y]]
- [ ] preview should require login
- [ ] admin: move content creation logic and defaults to `model.Content`
- [ ] admin: WYSIWYG editors
- [ ] admin: rst format
- [ ] admin: asciidoc format
- [ ] admin: media upload
- [ ] admin: actions
- [ ] admin: links in columns
- [ ] admin: solve select2 submit on enter problem
- [ ] admin: user management
- [ ] admin: make content type optional field (only when admin class do not provide a default)
- [ ] admin: scaffold to enable list editing
- [ ] admin: adapt ajax to pymongo
- [ ] admin: requires login by default
- [ ] admin: requires login if running external
- [ ] admin: load content formats from plugin
- [ ] cli: decorations
- [ ] cli: click completion
- [ ] cli: module custom commands
- [ ] cli: fetch modules
- [ ] cli: fetch themes
- [ ] cli: cookiecutter project
- [ ] cli: pack templates
- [ ] cli: deploy base system
- [ ] cli: deploy github
- [ ] cli: deploy ftp
- [ ] cli: deploy scp
- [ ] cli: deploy heroku
- [ ] cli: deploy pythonanywhere
- [ ] Docker
- [ ] themes: find a way to download single pelican-themes
- [ ] fix some pelican unrendered footers
- [ ] allow dynamic favicons
- [ ] create tinydb debug toolbar
- [ ] mdBook documentation
- [ ] replace `flit` and find a better way to release
- [ ] import scripts (quokka old, wordpress, feed)
- [ ] handle extensions for static file and generate it based on rules
