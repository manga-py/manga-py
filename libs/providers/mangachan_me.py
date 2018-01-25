
from libs.fs import dirname
from .provider import Provider


class MangaChanMe(Provider):

    _local_storage = None

    def _prepare_storage(self):
        if not self._local_storage:
            self._local_storage = {}

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        name = chapter.text_content().strip()
        idx = self.re.search('_v(\\d+)_ch(\\d+)', name).groups()
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        pass

    def get_manga_name(self) -> str:
        name = '\\.me/[^/]+/\\d+\\-(.+)\\.html'
        return self.re.search(name, self.get_url()).group(1)

    def loop_chapters(self):
        path = dirname(self.get_archive_path())
        url = self.get_current_chapter().get('href')
        self.save_file(url, path)

    def get_chapters(self):
        url = self.re.search('\\.me/[^/]+/(\\d+\\-.+\\.html)', self.get_url()).group(1)
        url = '{}/download/{}'.format(self.get_domain(), url)
        items = self.html_fromstring(url, 'table#download_table tr td + td > a')
        return items

    def prepare_cookies(self):
        self._prepare_storage()

    def get_files(self):
        return []

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaChanMe
