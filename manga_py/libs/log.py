import logging.config
import shutil
from pathlib import Path

import yaml

config_file = Path.home().resolve().joinpath('.manga-py').joinpath('.logger.config.yaml')

# if in-home-directory config not exists, copy this
if not config_file.is_file():
    config_file.parent.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent.parent.joinpath('.logger.config.yaml')
    shutil.copy(str(src), str(config_file))

with open('.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

