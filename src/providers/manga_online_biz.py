from src.provider import Provider
from src.fs import get_temp_path, rename, path_join, dirname


# Archive downloading example. Without images
class MangaOnlineBiz(Provider):

    chapter_url = ''

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'/download/[^/]+/.+?_(\d+)_(\d+)', self.chapter_url).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        name = self.get_manga_name()
        url = '{}/{}.html'.format(self.get_domain(), name)
        return self.http_get(url)

    def get_manga_name(self) -> str:
        return self.re.search(r'\.biz/([^/]+)(?:/|\.html)', self.get_url()).group(1)

    def get_arc_path(self):
        path = self.get_archive_name()
        name = dirname(self.get_archive_path())
        return path_join(path, name + '.zip')

    def download_volume(self, idx, url, manga_name):
        temp_path = get_temp_path('{:0>2}_{}-temp_arc.zip'.format(idx, manga_name))
        self.save_file(self.http().normalize_uri(url), temp_path)
        rename(temp_path, self.get_arc_path())

    def loop_chapters(self):
        volumes = self._storage['chapters']
        manga_name = self.get_manga_name()
        for idx, url in enumerate(volumes):
            # todo: skip manual
            self.chapter_url = url
            self.download_volume(idx, url, manga_name)

    def get_chapters(self):
        s, c = r'MangaChapter\((.+)\);', self.get_storage_content()
        items = self.json.loads(self.re.search(s, c).group(1))
        n = self.http().normalize_uri
        return [n(i.get('downloadUrl')) for i in items]

    def get_files(self):
        return []


main = MangaOnlineBiz
