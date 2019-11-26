#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import isfile

from manga_py.meta import *

REQUIREMENTS = [
    'lxml',
    'cssselect',
    'Pillow',
    'pycryptodome',
    'cloudscraper',
    'urllib3',
    'packaging',
    'pyexecjs',
    'loguru',
    'argcomplete',
    'tinycss',
    'peewee',
    'manga-py.providers',
]


if isfile('requirements.txt'):
    with open('requirements.txt', 'r') as f:
        REQUIREMENTS = f.read().split('\n')


release_status = '5 - Production/Stable'
if ~version.find('beta'):
    release_status = '4 - Beta'
if ~version.find('alpha'):
    release_status = '3 - Alpha'


setup(
    name='manga_py',
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    version=version,
    description='Universal assistant download manga.',
    long_description='Please see %s' % (repo_url,),
    author=author,
    author_email=author_email,
    url=repo_url,
    zip_safe=False,
    download_url='{}/archive/{}.tar.gz'.format(repo_url, version),
    keywords=['manga-downloader', 'manga', 'manga-py'],
    license='MIT',
    classifiers=[  # look here https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: %s' % (release_status,),
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'manga-py = manga_py:main',
        ]
    }
)