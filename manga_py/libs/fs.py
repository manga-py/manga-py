import tempfile
from os import name as os_name, getpid, access, W_OK
from pathlib import Path
from typing import Union

__dir_name = '.manga-py'


# __temp = 'temp_%s' % getpid()
__temp = 'temp'


def temp_path() -> Path:
    """
    Returns the path of the temporary files manga-py
    """
    path = Path(tempfile.gettempdir()).joinpath(__dir_name, __temp).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def root_path() -> Path:
    """
    Returns the root of the installation path manga-py
    """
    return Path(__file__).resolve().parent.parent


def user_path() -> Path:
    """
    Returns the root path of the system files manga-py
    """
    if os_name == 'nt':
        home = Path.home().joinpath('AppData', 'Roaming', __dir_name)
    else:
        home = Path.home().joinpath(__dir_name)
    home.mkdir(parents=True, exist_ok=True)
    return home


def get_disk_stat(_path: Path) -> dict:
    import os

    _path = _path.resolve()
    _path.mkdir(exist_ok=True)
    _path = str(_path)

    if hasattr(os, 'statvfs'):  # POSIX
        st = os.statvfs(_path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return {'total': total, 'used': used, 'free': free}

    elif os.name == 'nt':  # Windows
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
    else:
        raise NotImplementedError('Platform not supported')


def check_free_space(_path: Path, min_size: Union[int, str] = 100) -> bool:
    _stat = get_disk_stat(_path)
    if isinstance(min_size, str) and min_size.find('%'):
        min_size = int(min_size)
        _free = _stat['free'] / _stat['total']
        if (_free * 100) < min_size:
            return False
        return True
    else:
        _free = _stat['free'] / (2 << 19)  # 1Mb
        if _free < min_size:
            return False
        return True


def is_writable(path: Union[str, Path]):
    return access(str(path), W_OK)


# def get_storage_path() -> Path:
#     """
#     Returns the root of the installation path manga-py
#     """
#     _path = system_path().joinpath('storage')
#     _path.parent.mkdir(parents=True, exist_ok=True)
#     return _path


__all__ = ['temp_path', 'root_path', 'user_path', 'get_disk_stat', 'check_free_space', 'is_writable']
