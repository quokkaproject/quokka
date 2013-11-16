#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

import quokka

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()
                if not i.startswith("http")]

dependency_links = [i.strip() for i in open("requirements.txt").readlines()
                    if i.startswith("http")]

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Framework :: Flask",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: 2.6",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.md').read()
except:
    long_description = quokka.__description__

setup(name='quokka',
      version=quokka.__version__,
      description=quokka.__description__,
      long_description=long_description,
      classifiers=classifiers,
      keywords='quokka cms flask publishing mongodb',
      author=quokka.__author__,
      author_email=quokka.__email__,
      url='http://quokkaproject.org',
      download_url="https://github.com/pythonhub/quokka/tarball/master",
      license=quokka.__license__,
      packages=find_packages(exclude=('doc', 'docs',)),
      namespace_packages=['quokka'],
      package_dir={'quokka': 'quokka'},
      install_requires=REQUIREMENTS,
      dependency_links=dependency_links,
      scripts=['quokka/bin/quokka-admin.py'],
      include_package_data=True,
      test_suite='runtests')
