from lxml.etree import Element

from manga_py.exceptions import InvalidChapter
from manga_py.libs import fs
from ._file import BaseFile
from .file import File


class Chapter(BaseFile):
    _archive = None

    def __init__(self, idx, data, provider):
        super().__init__(idx, data, provider)
        self._location = fs.path_join(
            provider.arg('destination'),
            provider.manga_name
        )

    def _parse_data(self, data):
        if not isinstance(data, (dict, tuple, Element)):
            InvalidChapter(data)
        if isinstance(data, dict):
            self._url = data['url']
            name = data['name']
        elif isinstance(data, Element):
            self._url = self.provider.http.normalize_uri(data.get('src'))
            name = fs.basename(self._url)
            name = fs.remove_query(name)
        else:
            # ('absolute_url', 'archive_name/folder_name')
            self._url = data[0]
            name = data[1]
        self._name = self._normalize_name(name)

    def _normalize_name(self, name):
        if self.provider.arg('zero-fill') and isinstance(name, (list, tuple)):
            fmt = ('_{}' * (len(name) - 1))
            return ('vol_{:0>3}' + fmt).format(name)
        return name

    @property
    def file(self) -> File:  # FOR ARCHIVE DOWNLOAD
        if self._archive is None:
            AttributeError('Archive is None')
        return self.file
