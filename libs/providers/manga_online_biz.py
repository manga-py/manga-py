from .provider import Provider
from libs.fs import get_temp_path, rename, path_join


# Archive downloading example. Without images
class MangaOnlineBiz(Provider):

    chapter_url = ''

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re.search('/download/[^/]+/.+?_(\\d+)_(\\d+)', self.chapter_url).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        name = self.get_manga_name()
        url = '{}/{}.html'.format(self.get_domain(), name)
        return self.http_get(url)

    def get_manga_name(self) -> str:
        return self.re.search('\\.biz/([^/]+)(?:/|\\.html)', self.get_url()).group(1)

    def get_arc_path(self):
        name = self._params.get('name', '')
        if not len(name):
            name = self._storage['manga_name']

        _path = str(self.get_archive_name())
        return path_join(
            self._params.get('path_destination', 'Manga'),
            name,
            _path + '.zip'
        )

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
        json_data = self.re.search('MangaChapter\\((.+)\\);', self.get_main_content()).group(1)
        items = self.json.loads(json_data)
        return [self.get_domain() + i.get('downloadUrl') for i in items]

    def prepare_cookies(self):
        pass

    def get_files(self):
        return []

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaOnlineBiz
