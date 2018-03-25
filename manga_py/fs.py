import tempfile
from os import path, name as os_name, getpid, unlink as os_unlink, makedirs, stat
from pathlib import Path
from shutil import rmtree, move

__dir_name__ = '.PyMangaDownloader'


def get_temp_path(*args):
    temp = 'temp_%s' % getpid()
    return path.join(tempfile.gettempdir(), __dir_name__, temp, *args)


def root_path():
    return path.dirname(path.dirname(path.realpath(__file__)))


def get_util_home_path():
    if os_name == 'nt':
        home = path.join(str(Path.home()), 'AppData', 'Roaming', __dir_name__)
    else:
        home = path.join(str(Path.home()), __dir_name__)
    return home


def make_dirs(directory):
    path.isdir(directory) or makedirs(directory)


def remove_file_query_params(name, save_path: bool = True) -> str:
    file_path = path.dirname(name)
    name = path.basename(name)
    position = name.find('?')
    if position == 0:
        name = 'image.png'  # fake image name
    elif position > 0:
        name = name[:position]
    return path.join(file_path, name) if save_path else name


def is_file(_path):
    return path.isfile(_path)


def is_dir(_path):
    return path.isdir(_path)


def basename(_path):
    return path.basename(_path)


def dirname(_path):
    return path.dirname(_path)


def path_join(_path, *args):
    return path.join(_path, *args)


def unlink(_path):
    if is_dir(_path):
        return rmtree(_path)
    if is_file(_path):
        return os_unlink(_path)


def os_stat(_path):
    if is_file(_path):
        return stat(_path)
    return None


def file_size(_path):
    data = os_stat(_path)
    if data:
        return data.st_size
    return None


def rename(_from, _to):
    if is_file(_from) or is_dir(_from):
        is_dir(dirname(_to)) or makedirs(dirname(_to))
        move(_from, _to)


def storage(_path):
    _path = get_temp_path('storage', _path)
    make_dirs(dirname(_path))
    return _path
