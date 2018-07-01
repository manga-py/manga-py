import tempfile
from os import path, name as os_name, getpid, unlink as os_unlink, makedirs, stat, walk
from pathlib import Path
from shutil import rmtree, move
from json import loads as json_loads

__dir_name__ = '.manga-py'


def mark_as_hidden(_path: str):
    try:
        from ctypes import windll
        windll.kernel32.SetFileAttributesW(_path, 2)
    except Exception:
        pass


def get_temp_path(*args):
    temp = 'temp_%s' % getpid()
    return path.join(tempfile.gettempdir(), __dir_name__, temp, *args)


def root_path():
    return path.dirname(path.dirname(path.realpath(__file__)))


def get_util_home_path():
    if os_name == 'nt':
        home = path_join(str(Path.home()), 'AppData', 'Roaming', __dir_name__)
    else:
        home = path_join(str(Path.home()), __dir_name__)
    make_dirs(home)
    return home


def make_dirs(directory):
    is_dir(directory) or makedirs(directory)


def remove_query(name, save_path: bool = True) -> str:
    file_path = ''
    if ~name.find('/'):
        file_path = dirname(name)
        name = basename(name)
    position = name.find('?')
    if position == 0:
        raise AttributeError('Name is empty')
    elif position > 0:
        name = name[:position]
    return path.join(file_path, name) if save_path else name


def is_file(_path):
    return Path(_path).is_file()


def is_dir(_path):
    return Path(_path).is_dir()


def basename(_path):
    return path.basename(_path)


def dirname(_path):
    return path.dirname(_path)


def path_join(_path, *args):
    return Path.joinpath(_path, *args)


def unlink(_path):
    if is_dir(_path):
        return Path(_path).rmdir()
    if is_file(_path):
        return Path(_path).unlink()


def os_stat(_path):
    if is_file(_path):
        return stat(_path)
    return None


def file_size(_path):
    data = os_stat(_path)
    if data is not None:
        return data.st_size
    return -1


def rename(_from, _to):
    if is_file(_from) or is_dir(_from):
        is_file(_to) or make_dirs(_to)
        move(_from, _to)


def storage(_path, add_storage=True):
    _path = path_join(
        get_util_home_path(),
        ('storage' if add_storage else ''),
        _path
    )
    make_dirs(dirname(_path))
    return _path


def listing(_path) -> dict:
    """
    :param _path:
    :return: {'directories': [], 'files': []}
    """
    _dirname, _dirnames, _filenames = walk(_path)
    return {'directories': _dirnames, 'files': _filenames}


def __get_info(_path):
    try:
        with open(path_join(_path, 'info.json'), 'r') as r:
            return json_loads(r.read())
    except FileNotFoundError:
        return None


def get_info(_path) -> dict:
    """
    listing subdirectories and reading info.json files
    :param _path: [{..}, {..}, {..}]
    :return:
    """
    result = {}
    for d in listing(_path)['directories']:
        directory = path_join(_path, d)
        info = __get_info(directory)
        if info is not None:
            result[directory] = info
    return result
