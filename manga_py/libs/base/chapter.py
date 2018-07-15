from manga_py.libs import fs
from manga_py.exceptions import InvalidFile
from lxml.etree import Element


class Chapter:
    _idx = None
    _url = None
    _name = None
    _provider = None
    _http = None

    def __init__(self, idx, data, provider):
        self._idx = idx
        self._parse_data(data)
        self._provider = provider
        self._http = provider.http.copy()

    def _parse_data(self, data):
        assert isinstance(data, (tuple, Element)), InvalidFile(data)
        if isinstance(data, Element):
            self._url = self._provider.http.normalize_uri(data.get('src'))
            name = fs.basename(self._url)
            name = fs.remove_query(name)
        else:
            # ('absolute_url', 'archive_name/folder_name')
            self._url = data[0]
            name = data[1]
        self._name = self._normalize_name(name)

    def _normalize_name(self, name):
        if self._provider.arg('zero-fill') and isinstance(name, (list, tuple)):
            fmt = ('_{}' * (len(name) - 1))
            return ('vol_{:0>3}' + fmt).format(name)
        return name

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
        return fs.path_join(self._provider.arg('destination'), self.name)
