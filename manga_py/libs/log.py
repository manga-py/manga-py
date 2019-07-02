import logging
import logging.config
from logging import Logger
from pathlib import Path
from sys import stderr
from typing import Optional

__cache = {}


def _get(path: Path, name: str):
    config_file = path.resolve()
    config_file.touch()
    if not config_file.is_file():
        raise FileNotFoundError

    log = logging.getLogger(name)
    log.addHandler(logging.FileHandler(str(config_file)))

    return log


def _fake(name: str):
    log = logging.getLogger(name)
    log.addHandler(logging.StreamHandler(stderr))
    return log


def __get_logger(path, name):
    if path is None:
        return _fake(name)
    try:
        log = _get(Path(path), name)
    except (FileNotFoundError, ValueError):
        log = _fake(name)
        log.warning('Use stderr logger. Destination file is not writable')
    return log


def logger(path: Optional[str] = None, name: str = 'manga-py-logger') -> Logger:
    if __cache.get('logger') is None:
        __cache['logger'] = __get_logger(path, name)
    return __cache['logger']


__all__ = ['logger']
