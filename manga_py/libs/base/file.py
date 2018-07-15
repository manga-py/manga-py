from manga_py.libs import fs
from manga_py.exceptions import InvalidChapter
from lxml.etree import Element


class File:
    _idx = None
    _url = None
    _name = None
    _provider = None
    _http = None

    def __init__(self, idx, data, provider):
        self._idx = idx
        self._parse_data(data)
        self._provider = provider
        self._http = self._provider.http.copy()

    def _parse_data(self, data):
        assert isinstance(data, (tuple, Element)), InvalidChapter(data)
        if isinstance(data, Element):
            self._url = self._http.normalize_uri(data.get('src'))
            name = fs.basename(self._url)
            name = fs.remove_query(name)
        else:
            # ('absolute_url', 'relative_file_name')
            self._url = data[0]
            name = data[1]
        self._name = self._normalize_name(name)

    def _normalize_name(self, name):
        if self._provider.arg('rename_pages'):
            return '{:0>3}'.format(self._idx)
        return '{:0>3}_{}'.format(self._idx, name)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def url(self):
        return self._url

    @property
    def idx(self):
        return self._idx

    @property
    def path_location(self):
        return fs.path_join(self._provider.temp_path_location, self.name)
