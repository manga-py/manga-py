from manga_py.provider import Provider
from .helpers.std import Std
from manga_py.crypt import mangago_me


class MangaGoMe(Provider, Std):
    _enc_images = None
    _crypt = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        tp = self.re.search('/(\w{1,4})/[^/]*?\d+', self.chapter)
        idx = [self.chapter_id, idx[-1]]  # do not touch this!
        if tp:
            idx.append(tp.group(1))
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        selector = r'/\w{1,4}/[^/]*?(\d+)(?:[^\d]+(\d+))?'
        idx = self.re.search(selector, self.chapter).groups()
        if idx[1] is not None:
            fmt = '{}-{}'
            return fmt.format(*idx)
        return idx[0]

    def get_main_content(self):
        return self._get_content('{}/read-manga/{}/?av=1')

    def get_manga_name(self) -> str:
        return self._get_name(r'/read-manga/([^/]+)/')

    def get_chapters(self):
        content = self._elements('#information')
        if not content:
            return []
        chapters = content[0].cssselect('#chapter_table a.chico')
        raws = content[0].cssselect('#raws_table a.chicor')
        return chapters + raws

    def prepare_cookies(self):
        self._crypt = mangago_me.MangaGoMe()
        self.cf_protect(self.domain)

    def get_files(self):
        self._enc_images = []
        content = self.http(True, {
            'referer': self.chapter,
            'cookies': self.http().cookies,
            'user_agent': self.http().user_agent
        }).get(self.chapter)
        re = self.re.search(r"imgsrcs\s*=\s*['\"](.+)['\"]", content)
        if not re:
            return []
        items = self._crypt.decrypt(re.group(1))
        return items.split(',')

    def before_file_save(self, url, idx):
        if ~url.find('/cspiclink/'):
            self._enc_images.append(idx)
        return url

    def after_file_save(self, _path: str, idx: int):
        if idx in self._enc_images:
            print(idx)

    def get_cover(self):
        return self._cover_from_content('#information .cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaGoMe
