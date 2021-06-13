import tempfile
from json import loads as json_loads
from os import name as os_name, getpid, makedirs, walk
from pathlib import Path
from shutil import move
from shutil import rmtree

__dir_name__ = '.PyMangaDownloader'


def mark_as_hidden(_path: str):
    try:
        from ctypes import windll
        windll.kernel32.SetFileAttributesW(_path, 2)
    except Exception:
        pass


def get_temp_path(*args) -> str:
    temp = 'temp_%s' % getpid()
    return path_join(tempfile.gettempdir(), __dir_name__, temp, *args)


def root_path() -> str:
    #      fs.py/manga_py/../
    file = Path(__file__).resolve()
    return str(file.parent.parent)


def get_util_home_path() -> str:
    if os_name == 'nt':
        home = path_join(str(Path.home()), 'AppData', 'Roaming', __dir_name__)
    else:
        home = path_join(str(Path.home()), __dir_name__)
    make_dirs(home)
    return str(home)


def make_dirs(directory):
    is_dir(directory) or makedirs(directory)


def remove_file_query_params(name, save_path: bool = True) -> str:
    if name is None:
        raise AttributeError
    file_path = dirname(name)
    name = basename(name)
    position = name.find('?')
    if position == 0:
        name = 'image.png'  # fake image name
    elif position > 0:
        name = name[:position]
    return str(path_join(file_path, name) if save_path else name)


def is_file(_path) -> bool:
    return Path(_path).is_file()


def is_dir(_path) -> bool:
    return Path(_path).is_dir()


def basename(_path) -> str:
    return str(Path(_path).name)


def dirname(_path) -> str:
    return str(Path(_path).parent)


def path_join(_path, *args) -> str:
    return str(Path(_path).joinpath(*args))


def unlink(_path, allow_not_empty=False):
    if is_dir(_path):
        if allow_not_empty:
            rmtree(_path)
        else:
            Path(_path).rmdir()
    elif is_file(_path):
        Path(_path).unlink()


def os_stat(_path):
    if is_file(_path):
        return Path(_path).stat()
    return None


def file_size(_path):
    """
    :param _path:
    :return:
    :rtype: int
    """
    data = os_stat(_path)
    if data:
        return data.st_size
    return None


def rename(_from, _to):
    if is_file(_from) or is_dir(_from):
        is_dir(dirname(_to)) or makedirs(dirname(_to))
        move(_from, _to)


def storage(_path) -> str:
    _path = get_temp_path('storage', _path)
    make_dirs(dirname(_path))
    return str(_path)


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


def __dirname(_path) -> str:
    if not is_dir(_path):
        _path = __dirname(dirname(_path))
    return str(_path)


def _disk_stat_posix(_path) -> dict:
    import os
    st = os.statvfs(_path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return {'total': total, 'used': used, 'free': free}


def _disc_stat_win(_path) -> dict:
    import ctypes
    _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), ctypes.c_ulonglong()
    fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
    ret = fun(_path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
    if ret == 0:
        fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
        ret = fun(_path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
        if ret == 0:
            raise ctypes.WinError()
    used = total.value - free.value
    return {'total': total.value, 'used': used, 'free': free.value}


def get_disk_stat(_path) -> dict:
    import os
    _path = __dirname(_path)

    if hasattr(os, 'statvfs'):  # POSIX
        return _disk_stat_posix(_path)
    elif os.name == 'nt':  # Windows
        return _disc_stat_win(_path)
    else:
        raise NotImplementedError('Platform not supported')


def check_free_space(_path: str, min_size: int = 100, percent: bool = False) -> bool:
    """
    min_size = 10  # percent = True
    min_size = 10  # percent = False (default)

    :param _path:
    :param min_size:
    :param percent:
    :return:
    """
    _stat = get_disk_stat(_path)
    if percent:
        _free = _stat['free'] / _stat['total']
        if (_free * 100) < min_size:
            return False
        return True
    else:
        _free = _stat['free'] / (2 << 19)  # 1Mb
        if _free < min_size:
            return False
        return True


def touch(_path: str, mode=0o666, exist_ok=True):
    Path(_path).touch(mode, exist_ok)
