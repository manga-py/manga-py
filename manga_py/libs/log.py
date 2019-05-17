import logging.config
import shutil

import yaml

from manga_py.libs import fs

config_file = fs.system_path().joinpath('.logger.config.yaml')

# if in-home-directory config not exists, copy this
if not config_file.is_file():
    src = fs.root_path().joinpath('.logger.config.yaml')
    shutil.copy(str(src), str(config_file))

with open('.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

