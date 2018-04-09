from manga_py.fs import get_temp_path, rename, path_join, dirname
from manga_py.provider import Provider
from .helpers.std import Std


# Archive downloading example. Without images
class MangaOnlineBiz(Provider, Std):
    chapter_url = ''

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/download/[^/]+/.+?_(\d+)_(\d+)', self.chapter_url).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        return self._get_content('{}/{}.html')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.biz/([^/]+)(?:/|\.html)')

    def get_arc_path(self):
        path = self.get_archive_name()
        name = dirname(self.get_archive_path())
        return path_join(path, name + '.zip')

    def download_volume(self, idx, url, manga_name):
        temp_path = get_temp_path('{:0>2}_{}-temp_arc.zip'.format(idx, manga_name))
        self.save_file(self.http().normalize_uri(url), temp_path)
        rename(temp_path, self.get_arc_path())

    def loop_chapters(self):
        _min = self._params.get('skip_volumes', 0)
        _max = _min + self._params.get('max_volumes', 0)
        volumes = self._storage['chapters']
        for idx, url in enumerate(volumes):
            if idx < _min or (idx > _max > 0) or self._check_archive():
                continue
            self.chapter_url = url
            self.download_volume(idx, url, self.manga_name)

    def get_chapters(self):
        s, c = r'MangaChapter\((.+)\);', self.content
        items = self.json.loads(self.re.search(s, c).group(1))
        n = self.http().normalize_uri
        return [n(i.get('downloadUrl')) for i in items]

    def get_files(self):
        return []

    def get_cover(self):
        return self._cover_from_content('.item > .image > img')


main = MangaOnlineBiz
