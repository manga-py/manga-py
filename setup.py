from __future__ import print_function

from setuptools import setup
from glob import glob
from manga_py.meta import __version__, __downloader_uri__
from os.path import isfile


REQUIREMENTS = [
    'lxml>=3.7.2',
    'cssselect>=1.0.0',
    'Pillow>=4.3',
    'requests>=2.14',
    'pycrypto>=2.5',
    'cfscrape>=1.9.1',
    'PyQT5>=5.4',
    'progressbar2>3.34',
    'urllib3',
    'packaging',
    'html-purifier>=0.1.9',
]

long_description = ''
if isfile('README.rst'):
    with open('README.rst') as f:
        long_description = f.read()

setup(
    name='manga_py',
    packages=[
        'manga_py',
        'manga_py.base_classes',
        'manga_py.crypt',
        'manga_py.gui',
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
        ('manga_py/gui/langs', glob('manga_py/gui/langs/*.json'))
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
            'manga-py = manga_py:main',
        ]
    }
)
