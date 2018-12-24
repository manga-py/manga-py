#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import print_function

from os import path

from setuptools import setup

from manga_py import __author__, __email__, __license__
from manga_py.meta import __version__, __downloader_uri__

REQUIREMENTS = [
    'lxml',
    'cssselect',
    'Pillow',
    'requests',
    'pycrypto',
    'cfscrape',
    'progressbar2',
    'urllib3',
    'packaging',
    'pyexecjs>=1.5.1',
    'html-purifier',
]


# if path.isfile('requirements.txt'):
#     with open('requirements.txt') as f:
#         REQUIREMENTS = f.read()


long_description = ''
if path.isfile('README.rst'):
    with open('README.rst') as f:
        long_description = f.read()


release_status = 'Development Status :: 5 - Production/Stable'
if ~__version__.find('beta'):
    release_status = 'Development Status :: 4 - Beta'
if ~__version__.find('alpha'):
    release_status = 'Development Status :: 3 - Alpha'


setup(
    name='manga_py',
    packages=[
        'manga_py',
        'manga_py.base_classes',
        'manga_py.crypt',
        'manga_py.cli',
        'manga_py.http',
        'manga_py.providers',
        'manga_py.providers.helpers',
        'manga_py.server',
    ],
    include_package_data=True,
    version=__version__,
    description='Universal assistant download manga.',
    long_description=long_description,
    author=__author__,
    author_email=__email__,
    url=__downloader_uri__,
    zip_safe=False,
    data_files=[
        ('manga_py/storage', [
            'manga_py/storage/.passwords.json.dist',
            'manga_py/storage/.proxy.txt',
            'manga_py/crypt/aes.js',
            'manga_py/crypt/aes_zp.js',
        ]),
    ],
    download_url='{}/archive/{}.tar.gz'.format(__downloader_uri__, __version__),
    keywords=['manga-downloader', 'manga', 'manga-py'],
    license=__license__,
    classifiers=[  # look here https://pypi.python.org/pypi?%3Aaction=list_classifiers
        release_status,
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.5',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'manga-py = manga_py:main',
        ]
    }
)
