from manga_py.provider import Provider
from .helpers.std import Std


class AllHentaiRu(Provider, Std):

    def get_archive_name(self):
        name = self.re.search('/.+/([^/]+/[^/]+)/?', self.chapter)
        return self.normal_arc_name({'vol': name.group(1).split('/', 2)})

    def get_chapter_index(self):
        name = self.re.search('/.+/(?:vol)?([^/]+/[^/]+)/?', self.chapter)
        return name.group(1).replace('/', '-')

    def get_content(self):
        return self._get_content('{}/{}?mature=1&mtr=1')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        return self._elements('.expandable.chapters-link tr > td > a')

    def get_files(self):
        # Currently doesn't work; I assume viewer was changed, the following does not look like the current structure.
        _uri = self.http().normalize_uri(self.chapter)
        content = self.http_get(_uri)
        result = self.re.search(r'var pictures.+?(\[\{.+\}\])', content, self.re.M)
        if not result:
            return []
        content = result.group(1).replace("'", '"')
        content = self.re.sub('(\w*):([^/])', r'"\1":\2', content)
        return [i['url'] for i in self.json.loads(content)]

    def get_cover(self):
        return self._cover_from_content('.picture-fotorama > img')

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _path = None
        try:
            _path = super().save_file(idx, callback, url, in_arc_name)
        except AttributeError:
            pass
        if _path is None:
            for i in ['a', 'b', 'c']:
                try:
                    _path, idx, _url = self._save_file_params_helper(url, idx)
                    _url = self.re.sub(r'//\w\.', '//%s.' % i, url)

                    self.http().download_file(_url, _path, idx)
                    callable(callback) and callback()
                    self.after_file_save(_path, idx)

                    self._archive.lazy_add(_path)
                    break
                except AttributeError:
                    pass
        return _path

    def book_meta(self) -> dict:
        # todo meta
        pass


main = AllHentaiRu
