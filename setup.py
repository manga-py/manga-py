from __future__ import print_function

from setuptools import setup
from setuptools.command.install import install
from manga_py import meta
from os import name, chmod, unlink
from subprocess import Popen, PIPE
from re import search
from tempfile import gettempdir
from sys import stderr
from pathlib import Path


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
    'pyexecjs',
    'html-purifier',
    'peewee',
    'better_exceptions',
]


def walk(_path: str) -> tuple:
    """
    :param _path:
    :return: tuple(_path, tuple('dirs',), tuple('files',))
    """
    dirs = []
    files = []
    path = Path(_path)
    for i in path.iterdir():
        if i.is_file():
            files.append(str(i))
        if i.is_dir():
            dirs.append(str(i))
    return path.resolve(), dirs, files


# generate manga_py/libs/modules/html/templates/__init__.py
def generate_html_template():
    data_files = 'manga_py/libs/modules/html/templates'
    pass


if Path('requirements.txt').is_file():
    with open('requirements.txt') as f:
        REQUIREMENTS = f.read()


long_description = ''
if Path('README.rst').is_file():
    with open('README.rst') as f:
        long_description = f.read()


release_status = 'Development Status :: 1 - Planning'
# release_status = 'Development Status :: 5 - Production/Stable'
# if ~__version__.find('beta'):
#     release_status = 'Development Status :: 4 - Beta'
# if ~__version__.find('alpha'):
#     release_status = 'Development Status :: 3 - Alpha'


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    @staticmethod
    def _make_sh(_temp_file, complete_sh):
        with open(_temp_file, 'w') as f:
            f.write(''.join([
                '#!/bin/sh\n',
                'if [ `cat ~/.bashrc | grep {0} | wc -l` -lt 1 ];',
                ' then echo ". {0}" >> ~/.bashrc &&',
                ' echo "Please, restart you shell"; fi'
            ]).format(complete_sh))
        chmod(_temp_file, 0o755)

    @staticmethod
    def _parse_out(out):
        if isinstance(out, bytes):
            out = out.decode()
        _sh = search(r'\w\s(/.+?\.sh)', out)
        return _sh.group(1)

    def run(self):
        install.run(self)
        if name.find('nt') == -1:
            print_function('Activate argcomplete')
            process = Popen([
                'activate-global-python-argcomplete',
                '--user'
            ], stdout=PIPE, stderr=PIPE)
            out, err = process.communicate(timeout=1)
            if process.returncode == 0:
                sh = self._parse_out(out)
                _temp_file = Path(gettempdir()).joinpath('manga-py.sh')
                self._make_sh(_temp_file, sh)
                Popen([_temp_file]).communicate(timeout=1)
                unlink(_temp_file)
            else:
                print_function('ERROR! %s' % err, file=stderr)


setup(  # https://setuptools.readthedocs.io/en/latest/setuptools.html#namespace-packages
    name='manga_py',
    packages=[
        'manga_py',
        'manga_py.cli',
        'manga_py.cli.args',
        'manga_py.libs',
        'manga_py.libs.base',
        'manga_py.libs.crypt',
        'manga_py.libs.http',
        'manga_py.libs.modules',
        'manga_py.libs.modules.html',
        'manga_py.libs.modules.html.templates',
        'manga_py.providers',
    ],
    include_package_data=True,
    version=meta.__version__,
    description='Universal assistant download manga.',
    long_description=long_description,
    author=meta.__author__,
    author_email=meta.__email__,
    url=meta.__download_uri__,
    zip_safe=True,
    data_files=[],
    download_url='{}/archive/{}.tar.gz'.format(meta.__download_uri__, meta.__version__),
    keywords=['manga-downloader', 'manga', 'manga-py', 'manga-dl'],
    license=meta.__license__,
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
    python_requires='>=3.5.3',
    install_requires=REQUIREMENTS,
    cmdclass={
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'manga-py = manga_py:main',
            'manga-py-db = manga_py:db',
        ]
    },
    test_suite='tests',
)
