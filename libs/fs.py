from os import path, name as os_name
import tempfile
from pathlib import Path


__dir_name__ = '.PyMangaDownloader'


def get_temp_path(*args):
    return path.join(tempfile.gettempdir(), __dir_name__, 'temp', *args)


def get_current_path():
    return path.dirname(path.dirname(path.realpath(__file__)))


def get_util_home_path():
    if os_name == 'nt':
        home = path.join(str(Path.home()), 'AppData', 'Roaming', __dir_name__)
    else:
        home = path.join(str(Path.home()), __dir_name__)
    return home
