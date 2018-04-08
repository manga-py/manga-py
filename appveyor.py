from cx_Freeze import setup, Executable
from manga_py.meta import __version__

base = None

executables = [Executable('manga.py', base=base)]

packages = [
    'idna',

    'manga_py',
    'manga_py.base_classes',
    'manga_py.crypt',
    'manga_py.gui',
    'manga_py.http',
    'manga_py.providers',
    'manga_py.providers.helpers',
    'manga_py.server',
]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name='manga-py',
    options=options,
    version=__version__,
    description='Manga downloader',
    executables=executables
)
