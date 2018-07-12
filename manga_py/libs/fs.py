import tempfile
from os import name as os_name, getpid
from pathlib import Path
import json

__dir_name = '.manga-py'


def get_temp_path(*args) -> str:
    """
    Returns the path of the temporary files manga-py
    :param args:
    :return:
    """
    temp = 'temp_%s' % getpid()
    return path_join(tempfile.gettempdir(), __dir_name, temp, *args)


def root_path() -> str:
    """
    Returns the root of the installation path manga-py
    :return:
    """
    _root = Path(__file__).resolve()
    return str(_root.parent.parent)


def get_util_home_path() -> str:
    """
    Returns the root path of the system files manga-py
    :return:
    """
    if os_name == 'nt':
        home = path_join(str(Path.home()), 'AppData', 'Roaming', __dir_name)
    else:
        home = path_join(str(Path.home()), __dir_name)
    make_dirs(home)
    return str(home)


def make_dirs(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)


def remove_query(name: str) -> str:
    position = name.find('?')
    if position > 0:
        name = name[:position]
    return name


def is_file(_path) -> bool:
    return Path(_path).is_file()


def is_dir(_path) -> bool:
    return Path(_path).is_dir()


def basename(_path) -> str:
    return Path(_path).name


def dirname(_path) -> str:
    return str(Path(_path).parent)


def path_join(_path, *args) -> str:
    return str(Path(_path).joinpath(*args))


def unlink(_path):
    if is_dir(_path):
        Path(_path).rmdir()
    if is_file(_path):
        Path(_path).unlink()


def os_stat(_path):
    if is_file(_path):
        return Path(_path).stat()
    return None


def file_size(_path):
    data = os_stat(_path)
    if data is not None:
        return data.st_size
    return -1


def rename(_from, _to):
    Path(_from).rename(_to)


def storage(_path):
    """
    Returns the root of the installation path manga-py
    :return:
    """
    _path = path_join(get_util_home_path(), 'storage', _path)
    make_dirs(dirname(_path))
    return _path


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
            files.append(i)
        if i.is_dir():
            dirs.append(i)
    return path.resolve(), dirs, files


def listing(_path) -> dict:
    """
    :param _path:
    :return: {'directories': (,), 'files': (,)}
    """
    _dirname, _dirnames, _filenames = walk(_path)
    return {'directories': _dirnames, 'files': _filenames}


def __get_info(_path, result: dict):
    file = path_join(_path, 'info.json')
    if is_file(file):
        with open(file, 'r') as r:
            result[_path] = json.loads(r.read())


def get_info(_path: str) -> dict:
    """
    listing subdirectories and reading info.json files
    :param _path:
    :return:
    """
    result = {}
    for d in listing(_path)['directories']:
        directory = path_join(_path, d)
        __get_info(directory, result)
    return result
