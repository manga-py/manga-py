import logging
import logging.config
from logging import Logger
from pathlib import Path
from typing import Optional, Union

from manga_py.libs.fs import is_writable

__cache = {}


def _get(path: Path, name: str):
    config_file = path.resolve()
    config_file.touch()
    if not config_file.is_file() or not is_writable(config_file):
        raise FileNotFoundError

    logging.basicConfig(format='[%(levelname)s] (%(filename)s:%(lineno)d) %(message)s',)
    log = logging.getLogger(name)
    log.addHandler(logging.FileHandler(str(config_file)))

    return log


def _fake(name: str):
    log = logging.getLogger(name)
    log.addHandler(logging.StreamHandler())
    return log


def _file_logger(path, name):
    if path is None:
        return _fake(name)
    try:
        log = _get(Path(path), name)
    except (FileNotFoundError, ValueError):
        log = _fake(name)
        log.warning('Use stderr logger. Destination file is not writable')
    return log


def set_logger(_logger):
    __cache['logger'] = _logger


def logger(path: Optional[str] = None, name: str = 'manga-py-logger') -> Union[Logger, object]:
    if __cache.get('logger') is None:
        __cache['logger'] = _file_logger(path, name)
    if path is None:
        return __cache['logger']

    return __cache['logger']


__all__ = ['logger']
