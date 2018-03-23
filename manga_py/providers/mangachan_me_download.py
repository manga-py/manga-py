from manga_py.fs import dirname, path_join, get_temp_path, rename
from manga_py.provider import Provider
from .helpers.std import Std


class MangaChanMe(Provider, Std):
    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        name = r'\.me/[^/]+/\d+-(.+)\.html'
        return self._get_name(name)

    def loop_chapters(self):
        arc_name = self.get_archive_name()
        path = path_join(dirname(self.get_archive_path()), arc_name + '.zip')
        url = self.chapter
        temp_path = get_temp_path('{:0>2}_{}-temp_arc.zip'.format(self._storage['current_chapter'], arc_name))
        self.save_file(url, temp_path)
        rename(temp_path, path)

    def get_chapters(self):
        selector = r'\.me/[^/]+/(\d+-.+\.html)'
        url = self._get_name(selector)
        url = '/download/{}'.format(url)
        return self.html_fromstring(url, 'table#download_table tr td + td > a')

    def get_files(self):
        return []

    def get_cover(self):
        selector = r'\.me/[^/]+/(\d+-.+\.html)'
        url = self._get_name(selector)
        url = '{}/manga/{}'.format(self.domain, url)
        img = self._elements('#cover', self.http_get(url))
        if img and len(img):
            return img[0].get('src')


main = MangaChanMe
