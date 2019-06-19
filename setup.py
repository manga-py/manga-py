from setuptools import setup, find_packages
from setuptools.command.install import install
from manga_py import meta
from os import name, chmod, unlink
from subprocess import Popen, PIPE
from re import search
from tempfile import gettempdir
from sys import stderr, exit
from pathlib import Path


cur_dir = Path(__file__).resolve().parent # type: Path

REQUIREMENTS = [
    'lxml>=3.7.2',
    'cssselect>=1.0.0',
    'Pillow>=4.3',
    'requests>=2.21',
    'pycryptodome>=3.5',
    'cloudscraper>=1.1.1',
    'progressbar2>3.34',
    'urllib3',
    'packaging>=17',
    'html-purifier>=0.1.9',
    'js2py>=0.60',
    'peewee>3.4.0',
    'tinycss>=0.4',
    'better_exceptions>=0.2',
    'argcomplete>=1.9.4',
    'tabulate>=0.8',
    'PyYAML',
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


if cur_dir.joinpath('requirements.txt').is_file():
    with open('requirements.txt') as f:
        REQUIREMENTS = f.readlines()


long_description = ''
if cur_dir.joinpath('README.rst').is_file():
    with open('README.rst') as f:
        long_description = f.read()


release_status = 'Development Status :: 1 - Planning'
# release_status = 'Development Status :: 5 - Production/Stable'
# if ~meta.__version__.endswith('-beta'):
#     release_status = 'Development Status :: 4 - Beta'
# elif ~meta.__version__.endswith('-alpha'):
#     release_status = 'Development Status :: 3 - Alpha'


def _parse_out(out):
    if isinstance(out, bytes):
        out = out.decode()
    _sh = search(r'\w\s(/.+?\.sh)', out)
    return _sh.group(1)


def _make_sh(_temp_file, complete_sh):
    """Post-installation for installation mode."""
    with open(_temp_file, 'w') as f:
        f.write(''.join([
            '#!/bin/sh\n',
            'if [ `cat ~/.bashrc | grep {0} | wc -l` -lt 1 ];',
            ' then echo ". {0}" >> ~/.bashrc &&',
            ' echo "Please, restart you shell"; fi'
        ]).format(complete_sh))
    chmod(_temp_file, 0o755)


class PostInstallCommand(install):

    def run(self):
        install.run(self)
        if name.find('nt') == -1:
            print('Activate argcomplete')
            process = Popen([
                'activate-global-python-argcomplete',
                '--user'
            ], stdout=PIPE, stderr=PIPE)
            out, err = process.communicate(timeout=1)
            if process.returncode == 0:
                sh = _parse_out(out)
                _temp_file = str(Path(gettempdir()).joinpath('manga-py.sh'))
                _make_sh(_temp_file, sh)
                Popen([_temp_file]).communicate(timeout=1)
                unlink(_temp_file)
            else:
                print('ERROR! %s' % err, file=stderr)
                exit(1)


setup(  # https://setuptools.readthedocs.io/en/latest/setuptools.html#namespace-packages
    name='manga_py',
    packages = find_packages(),
    include_package_data=True,
    version=meta.__version__,
    description='Universal assistant download manga.',
    long_description=long_description,
    # long_description_content_type='text/markdown',
    author=meta.__author__,
    author_email=meta.__email__,
    url=meta.__download_uri__,
    zip_safe=True,
    data_files=[],  # look here https://docs.python.org/2/distutils/sourcedist.html#commands
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
            'manga-py-db = manga_py:db_main',
        ]
    },
    test_suite='tests',
)
