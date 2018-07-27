from lxml.etree import Element

from manga_py.exceptions import InvalidChapter
from manga_py.libs import fs
from ._file import BaseFile


class File(BaseFile):
    def __init__(self, idx, data, provider):
        super().__init__(idx, data, provider)
        self._location = self._provider.temp_path_location

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
        if self._provider.arg('rename-pages'):
            return '{:0>3}'.format(self._idx)
        return '{:0>3}_{}'.format(self._idx, name)
