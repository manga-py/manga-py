from os import path, makedirs
import json
from libs import fs


class ConfigStorage:

    __config_path = ''
    __storage = {}
    __lang = {}

    def __init__(self):
        self.__init_config_path()
        self.__load_config()
        self.__load_lang(self.__storage['lang'])

    def __init_config_path(self):
        self.__config_path = path.join(fs.get_util_home_path(), 'config.json')

    @staticmethod
    def __read_json_config(f):
        try:
            _json = json.loads(''.join(f.readlines()))
        except json.JSONDecodeError:
            _json = {}
        return _json

    def __load_config(self):
        if not path.isfile(self.__config_path):
            # make default config
            config_path = path.dirname(self.__config_path)
            path.isdir(config_path) or makedirs(config_path)
            with open(self.__config_path, 'w') as f:
                f.write(json.dumps({
                    'lang': 'en',
                }))
            self.__storage['lang'] = 'en'
            self.__storage['url'] = ''

        else:
            # load config
            with open(self.__config_path) as f:
                _json = self.__read_json_config(f)
                self.__storage = _json
                self.__storage['lang'] = getattr(_json, 'lang', 'en')
                self.__storage['url'] = getattr(_json, 'lang', '')

    def __load_lang(self, key):
        _path = path.join(fs.get_current_path(), 'helpers', '.gui.lang.{}.json')
        if not path.isfile(_path.format(key)):
            key = 'en'
        _path = _path.format(key)
        with open(_path) as f:
            self.__lang = self.__read_json_config(f)

    def get_param(self, key, default=None):
        """
        :param key: str
        :param default: str
        :return: mixed
        """
        return getattr(self, key, default)

    def set_param(self, key, value):
        self.__storage[key] = value

    def get_label(self, name):
        return self.get_param('label_{}'.format(name))

    def get_button(self, name):
        return self.get_param('button_{}'.format(name))

    def save_lang(self, key):
        pass

    def load_lang(self, key):
        pass

    def get_config(self):
        if hasattr(self.__storage, 'config'):
            return self.__storage['config']
        with open(self.__config_path) as f:
            config = self.__read_json_config(f)
            self.__storage['config'] = config['config']
            return config['config']

    def save_config(self):
        with open(self.__config_path, 'w') as f:
            f.write(json.dumps(self.__storage))
