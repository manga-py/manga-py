from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.crypt.base_lib import BaseLib


class MangaHereCc(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        selector = r'/manga/[^/]+/[^\d]+(\d+)/[^\d]+(\d+)'
        idx = self.re.search(selector, chapter)
        if idx:
            return '-'.join(idx.groups())
        selector = r'/manga/[^/]+/[^\d]+(\d+)'
        return self.re.search(selector, chapter).group(1)

    def get_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)')

    def get_chapters(self):
        return self._elements('.detail-main-list a')

    def get_files(self):
        content = self.http_get(self.chapter)
        chapter_id = self.re.search(r'(?:var)?\s+chapterid\s*=\s*(\d+);', content).group(1)
        guid_key = self.guid_key(content)

        pages = int(self.document_fromstring(content, '.pager-list-left span > a', -2).get('data-page'))
        chapter_url = self.re.search(r'^(.+/c\d+(?:\.\d+))/', self.chapter).group(1)

        n = self.http().normalize_uri
        return [n(i) for i in self._parse_images(pages, chapter_url, chapter_id, guid_key)]

    def guid_key(self, content):
        js = self.re.search(r'>\s*eval(\(function.+\))\s*<', content).group(1)
        key = BaseLib.exec_js('var j=' + js, 'j').split(';')
        return BaseLib.exec_js(key[0], 'guidkey')

    def _parse_images(self, pages, chapter_url, chapter_id, guid_key):
        images = []
        for page in range(0, pages + 1, 2):
            images_content = self.http_get('{}/chapterfun.ashx?cid={}&page={}&key={}'.format(
                chapter_url,
                chapter_id,
                page,
                guid_key,
            ))
            js = self.re.search(r'eval\((.+)\)', images_content).group(1)
            img = BaseLib.exec_js(BaseLib.exec_js('var _p = ' + js, '_p'), 'd')
            for i in img:
                if i not in images:
                    images.append(i)
        return images

    def get_cover(self):
        return self._cover_from_content('.detail-info-cover-img')

    def prepare_cookies(self):
        self._base_cookies()
        self.http().cookies['isAdult'] = '1'


main = MangaHereCc
