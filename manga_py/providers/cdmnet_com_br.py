from lxml import html

from manga_py.provider import Provider
from .helpers.std import Std


class CdmNetComBr(Provider, Std):

    def get_archive_name(self) -> str:
        url = self.chapter
        idx = self.get_chapter_index()
        if ~url.find('/manga/'):
            return 'vol_{:0>3}'.format(idx)
        if ~url.find('/novel/'):
            return 'novel_{:0>3}'.format(idx)

    def get_chapter_index(self) -> str:
        re = self.re.compile('/titulos/[^/]+/[^/]+/[^/]+/([^/]+)')
        return re.search(self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/titulos/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'/titulos/([^/]+)')

    def get_chapters(self):
        return self._elements('.ui .content .table td > a')

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        if ~url.find('/manga/'):
            return super().save_file(idx, callback, url, in_arc_name)
        if ~url.find('/novel/'):
            _path, idx, _url = self._save_file_params_helper(url, idx)
            _path += '.html'
            element = self.html_fromstring(url, '.novel-chapter', 0)
            with open(_path, 'wb') as f:
                f.write(html.tostring(element))
            callable(callback) and callback()
            self.after_file_save(_path, idx)
            self._archive.add_file(_path, in_arc_name)
            return _path

    def _manga(self):
        file_type = '.jpg'
        content = self.http_get(self.chapter)
        re_suffix = self.re.compile(r'urlSulfix\s*=\s*[\'"](.+)[\'"]\s*;')
        re_images = self.re.compile(r'pages\s*=\s*(\[.+\])\s*;')
        suffix = re_suffix.search(content).group(1)
        images = re_images.search(content).group(1)
        images = self.re.sub("'", '"', images)
        images = self.json.loads(self.re.sub(r'",\]', '"]', images))

        print(['{}{}{}'.format(suffix, i, file_type) for i in images]);
        exit()

        return ['{}{}{}'.format(suffix, i, file_type) for i in images]

    def get_files(self):
        if ~self.chapter.find('/manga/'):
            return self._manga()
        if ~self.chapter.find('/novel/'):
            return [self.chapter]
        return []

    def get_cover(self) -> str:
        return self._cover_from_content('.content .description img.image')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = CdmNetComBr
