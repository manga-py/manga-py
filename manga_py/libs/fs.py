import tempfile
from os import name as os_name, getpid
from pathlib import Path

__dir_name = '.manga-py'


__temp = 'temp_%s' % getpid()


def get_temp_path() -> Path:
    """
    Returns the path of the temporary files manga-py
    """
    path = Path(tempfile.gettempdir()).joinpath(__dir_name, __temp)
    path.mkdir(parents=True, exist_ok=True)
    return path


def root_path() -> Path:
    """
    Returns the root of the installation path manga-py
    """
    return Path(__file__).resolve().parent.parent


def system_path() -> Path:
    """
    Returns the root path of the system files manga-py
    """
    if os_name == 'nt':
        home = Path.home().joinpath('AppData', 'Roaming', __dir_name)
    else:
        home = Path.home().joinpath(__dir_name)
    home.mkdir(parents=True, exist_ok=True)
    return home


# def get_storage_path() -> Path:
#     """
#     Returns the root of the installation path manga-py
#     """
#     _path = system_path().joinpath('storage')
#     _path.parent.mkdir(parents=True, exist_ok=True)
#     return _path
