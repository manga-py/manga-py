from pathlib import Path
import os
import tempfile
from typing import Union

__dir_name = '.manga-py'


def is_readable(location: Path):
    if location.is_file():
        assert os.access(str(location), os.R_OK)


def is_writable(location: Path):
    assert os.access(str(location), os.W_OK)


def touch(location: Path):
    location = location.resolve()
    location.touch(mode=0o666)
    is_readable(location)


def user_path() -> Path:
    """
    Returns the root path of the system files manga-py
    """
    if os.name == 'nt':
        home = Path.home().joinpath('AppData', 'Roaming', __dir_name)
    else:
        home = Path.home().joinpath(__dir_name)
    home.mkdir(parents=True, exist_ok=True)
    return home


def temp_path() -> Path:
    """
    Returns the path of the temporary files manga-py
    """
    path = Path(tempfile.gettempdir()).joinpath(__dir_name).resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_disk_stat(_path: Path) -> dict:
    _path = _path.resolve()
    _path.mkdir(parents=True, exist_ok=True)
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
        return (_free * 100) > min_size
    else:
        _free = _stat['free'] / (2 << 19)  # 1Mb
        return _free > min_size
