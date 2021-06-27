from toml import load, dump
from . import DefaultConfig, CONFIG_FILE


def load_config() -> DefaultConfig:
    if not CONFIG_FILE.is_file():
        return DefaultConfig()

    with CONFIG_FILE.open('r') as r:
        data = load(r)
        return DefaultConfig(data.get('default', {}))


def dump_config(config: DefaultConfig):
    with CONFIG_FILE.open('r') as r:
        data = load(r)

    data['default'] = config.get_all()

    with CONFIG_FILE.open('w') as w:
        dump(data, w)
