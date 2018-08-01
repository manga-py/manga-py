from abc import abstractmethod

from manga_py.libs import fs


class BaseFile(object):
    _idx = None
    _url = None
    _name = None
    _provider = None
    _http = None
    _location = None

    def __init__(self, idx, data, provider):
        self._idx = idx
        self._parse_data(data)
        self._provider = provider
        self._http = self._provider.http.copy()

    @abstractmethod
    def _parse_data(self, data):
        pass

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
        return fs.path_join(self._location, self._name)

    @path_location.setter
    def path_location(self, location):
        self._location = location
