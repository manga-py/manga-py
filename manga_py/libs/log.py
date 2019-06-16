import logging.config
import shutil
from logging import Logger

import yaml

from manga_py.libs import fs

__cache = {}


def _get():
    config_file = fs.system_path().joinpath('.logger.config.yaml')

    # if in-home-directory config not exists, copy this
    if not config_file.is_file():
        src = fs.root_path().joinpath('.logger.config.yaml')
        shutil.copy(str(src), str(config_file))

    with open('.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

    return logging.getLogger(__name__)


def logger() -> Logger:
    if __cache.get('logger', None) is None:
        __cache['logger'] = _get()
    return __cache['logger']
