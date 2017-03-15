#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


with open('README.md') as readme_file:
    # TODO: convert to rst on release
    readme = readme_file.read()

with open('HISTORY') as history_file:
    history = history_file.read()

requirements = [
]

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
    url='https://github.com/rochacbruno/quokka',
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
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
