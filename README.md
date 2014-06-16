[![Flattr](http://api.flattr.com/button/flattr-badge-large.png)](http://flattr.com/thing/1680610/rochacbrunoquokka-on-GitHub)
[![Gittip](http://badgr.co/gittip/rochacbruno.png)](https://www.gittip.com/rochacbruno/)
[![Travis CI](http://badgr.co/travis-ci/pythonhub%2Fquokka.png)](https://travis-ci.org/pythonhub/quokka)
[![Coverage
Status](https://coveralls.io/repos/pythonhub/quokka/badge.png)](https://coveralls.io/r/pythonhub/quokka)
[![Twitter](http://badgr.co/twitter/@quokkaproject.png?bg=%2302779E)](http://twitter.com/quokkaproject)
[![Gitter chat](https://badges.gitter.im/pythonhub/quokka.png)](https://gitter.im/pythonhub/quokka)

Quokka project
===============================================

### Flask and MongoDB powered CMS
#### (alpha version, work in progress)

<p align="center">
<img src="docs/logo.png" alt="quokka cms" />
</p>


Quokka is a flexible content management platform powered by Python, Flask and MongoDB.


Quick start
============

> You need a MongoDB instance running locally or remotely to connect. 
> Quokka runs on Python 2.7

1. Get Quokka

```bash
$ git clone https://github.com/pythonhub/quokka
$ cd quokka
$ pip install -r requirements.txt
```

2. Define your MongoDB settings

```bash
$ $EDITOR quokka/local_settings.py
===============quokka/quokka/local_settings.py===============
MONGODB_SETTINGS = {'DB': 'your_mongo_db'}
DEBUG = True
=============================================================
```

3. Populate with sample data (optional)

```bash
$ python manage.py populate 

```

4. Create a superuser

```bash
$ python manage.py createsuperuser
you@email.com
P4$$W0Rd
```

5. Run

```bash
$ python manage.py runserver
```
6. Access on http://localhost:5000 
7. Admin on http://localhost:5000/admin

or by making your server reachable on other networks

```bash
$ python manage.py run0
```
6. Access on http://0.0.0.0:8000  
7. Admin on http://0.0.0.0:8000/admin


Docs on [Wiki](https://github.com/pythonhub/quokka/wiki)
===============================================

* [About & Features](https://github.com/pythonhub/quokka/wiki/about)
* [Installing and running](https://github.com/pythonhub/quokka/wiki/installation)
* [Requirements](https://github.com/pythonhub/quokka/wiki/requirements)
* [Extending & Installing modules](https://github.com/pythonhub/quokka/wiki/plugins)
* [Admin interface](https://github.com/pythonhub/quokka/wiki/screencast)
* [Project tree](https://github.com/pythonhub/quokka/wiki/project-tree)
* [Team & Commiters](https://github.com/pythonhub/quokka/graphs/contributors)


Hosting
=======

You can host a Quokka website in any VPS or cloud which supports Python and Flask + MongoDB access, a good option is to host the database in MongoLab if your hosting server does not provide Mongo.

- PythonAnywhere can run Quokka with Mongo hosted at MongoLab
- DigitalOcean is a good option for a VPS
- Jelastic Cloud has the easiest Quokka deployment - http://docs.jelastic.com/ru/quokka-cms

Is it any good?
==============

[Yes!](https://news.ycombinator.com/item?id=3067434)


![python](docs/python_powered.png)
&nbsp;
![flask](docs/flask_powered.png)
&nbsp;
![mongo](docs/mongo_powered.jpg)
&nbsp;
[![pythonhub](http://secure.gravatar.com/avatar/fa9ccd40c6da8a0a934a383ffeb988e6?s=78)](http://github.com/pythonhub)



## License
This project is licensed under the [MIT license](http://opensource.org/licenses/MIT).
