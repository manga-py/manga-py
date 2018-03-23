from __future__ import print_function

from setuptools import setup
from glob import glob
from manga_raw.meta import __version__, __downloader_uri__
from os.path import isfile


REQUIREMENTS = [
    'setuptools',
    'lxml>=3.7.2',
    'cssselect>=1.0.0',
    'Pillow>=4.3',
    'requests>=2.14',
    'pycrypto>=2.5',
    'cfscrape>=1.9.1',
    'progressbar2>3.34',
    'html-purifier>=0.1.9',
    'urllib3',
    'packaging',
]

long_description = ''
if isfile('README.rst'):
    with open('README.rst') as f:
        long_description = f.read()

setup(
    name='manga_raw',
    packages=[
        'manga_raw',
        'manga_raw.base_classes',
        'manga_raw.crypt',
        'manga_raw.gui',
        'manga_raw.http',
        'manga_raw.providers',
        'manga_raw.providers.helpers',
        'manga_raw.server',
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
        ('manga_raw/gui/langs', glob('manga_raw/gui/langs/*.json'))
    ],
    download_url='{}/archive/{}.tar.gz'.format(__downloader_uri__, __version__),
    keywords=['manga-downloader', 'manga'],
    license='MIT',
    classifiers=[  # look here https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.5',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'manga-raw = manga_raw:main',
        ]
    }
)
