from manga_py.libs import fs
from manga_py.exceptions import InvalidFile
from lxml.etree import Element


class File:
    _idx = None
    _url = None
    _name = None
    _name_arc = None
    _provider = None
    _path_location = fs.get_temp_path()

    def __init__(self, idx, data, provider):
        self._idx = idx
        self._parse_data(data)
        self._provider = provider

    def _parse_data(self, data):
        assert isinstance(data, (tuple, Element)), InvalidFile(data)
        if isinstance(data, Element):
            self._url = self._provider.http.normalize_uri(data.get('src'))
            name = fs.basename(self._url)
            self._name = self._name_arc = '{:0>3}_{}'.format(self._idx, fs.remove_query(name))
        else:
            self._url = data[0]
            self._name_arc = data[1][0]
            self._name = data[1][1]

    def _normalize_name(self):
        if self._provider.arg()  # TODO

    @property
    def name(self):
        return self._name

    @property
    def name_arc(self):
        return self._name_arc

    @property
    def url(self):
        return self._url

    @property
    def idx(self):
        return self._idx
