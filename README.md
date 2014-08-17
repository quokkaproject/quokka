[![Flattr](http://api.flattr.com/button/flattr-badge-large.png)](http://flattr.com/thing/1680610/rochacbrunoquokka-on-GitHub)
[![Gittip](http://img.shields.io/gittip/rochacbruno.svg)](https://www.gittip.com/rochacbruno/)
[![Travis CI](http://img.shields.io/travis/pythonhub/quokka.svg)](https://travis-ci.org/pythonhub/quokka)
[![Coverage Status](http://img.shields.io/coveralls/pythonhub/quokka.svg)](https://coveralls.io/r/pythonhub/quokka)
[![Twitter](http://img.shields.io/badge/twitter-@quokkaproject-green.svg)](http://twitter.com/quokkaproject)
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

## FAQ

### Why another CMS?

There is a large number of great CMS's in Python ecosystem (Plone, Opps, Mezannine, DjangoCMS etc), each one has its own patterns for extension development and theme management. A CMS can take a its role as "Product" or as "Platform" and for Quokka the idea is to play in both scenarios, The CMS should be easy to deploy, extensions and themes should be "drop-in", it should be easy to develop extensions and also it should use a "schema-free" database. Until Quokka there was no CMS filling all these needs.

### Why Flask?

Because Flask is Pythonic! In my research + experience it is the best framework to develop applications which rely on "pluggable features" thanks to its Blueprints and Extension patterns, also Flask plays well with any DB/ORM of choice. (see next question) 

### Why MongoDB?

Because database acheme migrations are no-happy for CMS and a Quokka CMS must be always happy to work with, so no-schema-migrations is needed with MongoDB! and Mongo is the easiest, flexible and most suitable NoSQL for CMS, also there is excelent extensions for Flask (MongoEngine and Flask-Admin) which supports MongoDB!

### Why the project is named "Quokka?"

Because it is the happiest animal in the world!

#### 20 FACTS ABOUT QUOKKAS

- 1. Happiest animal in the world because they are known for how much they smile.
- 2. They are marsupials
- 3. They live on rottnest island named after quokkas because a Dutch guy thought they were large rats. Rottnest means "rats nest"
- 4. They can climb trees
- 5. Herbivores-they eat leaves,stems,grass,etc;
- 6. They are nocturnal
- 7. They can live for long periods of time, living off of the fat stored in their tails lol
- 8. Females usually give birth once a year
- 9. Quokkas are old enough to have babies at 1.5 years old!!
- 10. Live 5-10 years
- 11. Declining population—logging, pollution, killed by foxes,pet dogs, pet cats, humans,etc;😭😭
- 12. They live in tall grass near water
- 13. Btw if you meet a quokka don't feed it anything due to declining population because it could affect them
- 14. Quokkas highest speed is 20mph
- 15. They don't chew food.they just swallow it
- 16. Closely related to the Rock Wallaby (in the picture^^^)
- 17. Scientific name is Setonix Brachyurus
- 18. Joey stays with mom for 35 weeks
- 19. Quokkas recycle a small amount of their bodies waste products
- 20. They create their own trails and paths to get food and runaway from predators.

## License
This project is licensed under the [MIT license](http://opensource.org/licenses/MIT), see `LICENSE` for more details.


