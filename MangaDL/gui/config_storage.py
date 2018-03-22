from MangaDL import fs
import json


class ConfigStorage:

    __config_path = ''
    __storage = None
    __lang = None
    __lang_idx = None
    __langs_list = None

    def __init__(self):
        self.__storage = {}
        self.__lang = {}
        self.__lang_idx = {}
        self.__init_config_path()
        self.__load_config()
        self.__load_lang(self.__storage.get('lang', 'en'))

    def __init_config_path(self):
        self.__config_path = fs.path_join(fs.get_util_home_path(), 'config.json')

    @staticmethod
    def __read_json_config(f):
        try:
            _json = json.loads(''.join(f.readlines()))
        except json.JSONDecodeError:
            _json = {}
        return _json

    def __save_config(self, values: dict):
        config_path = fs.dirname(self.__config_path)
        fs.is_dir(config_path) or fs.makedirs(config_path)
        values.setdefault('lang', 'en')
        values.setdefault('url', '')
        with open(self.__config_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(values))

    def __load_config(self):
        if not fs.is_file(self.__config_path):
            # make default config
            self.__save_config({})
            self.__storage['lang'] = 'en'
            self.__storage['url'] = ''

        else:
            # load config
            with open(self.__config_path, encoding='utf-8') as f:
                _json = self.__read_json_config(f)
                self.__storage = _json
                self.__storage['lang'] = _json.get('lang', 'en')
                self.__storage['url'] = _json.get('lang', '')

    def __load_lang(self, key):
        print(self.__storage['lang'])
        _path = fs.path_join(fs.get_current_path(), 'src', 'gui', 'langs', '{}.json')
        if not fs.is_file(_path.format(key)):
            key = 'en'
        _path = _path.format(key)
        with open(_path, encoding='utf-8') as f:
            self.__lang = self.__read_json_config(f)

    def get_param(self, key, default=None):
        return self.__storage.get(key, default)

    def set_param(self, key, value):
        self.__storage[key] = value

    def get_config(self):
        if self.__storage.get('config', None):
            return self.__storage['config']
        self.__load_config()
        return self.__storage['config']

    def save_config(self):
        self.__save_config(self.__storage)

    def translate(self, key):
        return self.__lang.get(key, key)

    def next_lang(self):
        langs = self.get_langs_list()
        idx = langs.index(self.__storage['lang']) + 1
        lang = langs[0]
        if idx < len(langs):
            lang = langs[idx]
        self.__storage['lang'] = lang
        self.__save_config(self.__storage)
        return lang

    def get_langs_list(self):
        if not self.__langs_list:
            _path = fs.path_join(fs.get_current_path(), 'src', 'langs', '_langs.json')
            with open(_path, encoding='utf-8') as f:
                self.__langs_list = json.loads(''.join(f.readlines()))
        return self.__langs_list
