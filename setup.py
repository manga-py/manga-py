#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import stderr

from setuptools import setup, find_packages

from manga_py.meta import _version, _downloader_uri, _author, _email, _license

REQUIREMENTS = [
    'cloudscraper~=1.2.33',
    'cssselect~=1.1.0',
    'lxml~=4.5.0',
    'packaging~=20.3',
    'Pillow~=7.1.1',
    'progressbar2~=3.50.1',
    'pycryptodome~=3.9.7',
    'PyExecJS~=1.5.1',
    'requests~=2.23.0',
    'better_exceptions~=0.2.2',
]


long_description = """
Universal manga downloader.

Please see https://github.com/manga-py/manga-py
"""

release_status = 'Development Status :: 5 - Production/Stable'
if ~_version.find('beta'):
    release_status = 'Development Status :: 4 - Beta'
if ~_version.find('alpha'):
    release_status = 'Development Status :: 3 - Alpha'


setup(
    name='manga_py',
    packages=find_packages(exclude=(
        'tests',
        '.github',
        'Manga',
        'helpers',
        'mypy_cache',
    )),
    include_package_data=True,
    version=_version,
    description='Universal assistant download manga.',
    long_description=long_description,
    author=_author,
    author_email=_email,
    url=_downloader_uri,
    zip_safe=False,
    data_files=[
        ('manga_py/storage', [
            'manga_py/storage/.passwords.json.dist',
            'manga_py/storage/.proxy.txt',
            'manga_py/crypt/aes.js',
            'manga_py/crypt/aes_zp.js',
        ]),
    ],
    download_url='{}/archive/{}.tar.gz'.format(_downloader_uri, _version),
    keywords=['manga-downloader', 'manga', 'manga-py'],
    license=_license,
    classifiers=[  # look here https://pypi.python.org/pypi?%3Aaction=list_classifiers
        release_status,
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.5.3',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'manga-py = manga_py.util:main',
        ]
    }
)

print('\n'.join((
    '\n\nPlease remember that all sites earn on advertising.',
    'Remember to visit them from your browser.',
    'Thanks!\n'
)), file=stderr)
