from __future__ import print_function

from setuptools import setup
from glob import glob
from manga_py.meta import __version__, __downloader_uri__
from os import path


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

long_description = ''
if path.isfile('README.rst'):
    with open('README.rst') as f:
        long_description = f.read()

setup(
    name='manga_py',
    packages=[
        'manga_py',
        'manga_py.base_classes',
        'manga_py.crypt',
        'manga_py.http',
        'manga_py.providers',
        'manga_py.providers.helpers',
        'manga_py.server',
    ],
    include_package_data=True,
    version=__version__,
    description='Universal assistant download manga.',
    long_description=long_description,
    author='Zharkov Sergey',
    author_email='sttv-pc@mail.ru',
    url=__downloader_uri__,
    zip_safe=False,
    data_files=[
        ('manga_py/gui/langs', glob('manga_py/gui/langs/*.json')),
        ('manga_py/storage', [
            'manga_py/storage/.passwords.json.dist',
            'manga_py/storage/.proxy.txt',
        ])
    ],
    download_url='{}/archive/{}.tar.gz'.format(__downloader_uri__, __version__),
    keywords=['manga-downloader', 'manga'],
    license='MIT',
    classifiers=[  # look here https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
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
