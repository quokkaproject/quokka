#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os

from setuptools import setup


def read(*names, **kwargs):
    """Read a file."""
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def parse_md_to_rst(file):
    """Read Markdown file and convert to ReStructured Text."""
    try:
        from m2r import parse_from_file
        return parse_from_file(file).replace(
            "artwork/", "http://198.27.119.65/"
        )
    except ImportError:
        # m2r may not be installed in user environment
        return read(file)


with open('HISTORY') as history_file:
    history = history_file.read()

readme = parse_md_to_rst("README.md") + '\n\n' + history

requirements = []

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

test_requirements = [
    'pytest>=2.9.2',
    'pytest-xdist>=1.14'
]

setup(
    name='quokka',
    version='1.0.0',
    description=(
        "Quokka CMS"
    ),
    long_description=readme + '\n\n' + history,
    author="Bruno Rocha",
    author_email='rochacbruno@gmail.com',
    url='https://github.com/quokkaproject/quokka',
    packages=['quokka'],
    package_dir={'quokka': 'quokka'},
    entry_points={
        'console_scripts': [
            'quokka=quokka.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='quokka',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
