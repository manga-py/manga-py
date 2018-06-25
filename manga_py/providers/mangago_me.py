from manga_py.provider import Provider
from .helpers.std import Std


class MangaGoMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        tp = self.re.search('/(\w{1,4})/[^/]*?\d+', self.chapter).group(1)
        idx = [self.chapter_id, idx[-1]]  # do not touch this!
        idx.append(tp)
        return self.normal_arc_name(idx)

    def get_chapter_index(self) -> str:
        selector = r'/\w{1,4}/[^/]*?(\d+)(?:[^\d]+(\d+))?'
        idx = self.re.search(selector, self.chapter).groups()
        if idx[1] is not None:
            fmt = '{}-{}'
            return fmt.format(*idx)
        return idx[0]

    def get_main_content(self):
        return self._get_content('{}/read-manga/{}/')

    def get_manga_name(self) -> str:
        self.log('NOT WORKED NOW! Wait update, please!')
        exit()
        return self._get_name(r'/read-manga/([^/]+)/')

    def get_chapters(self):
        content = self.document_fromstring(self.content, '#information', 0)
        chapters = content.cssselect('#chapter_table a.chico')
        raws = content.cssselect('#raws_table a.chicor')
        return chapters + raws

    def prepare_cookies(self):
        self.cf_protect(self.get_url())

    def get_files(self):
        # content = self.http(True, {
        #     'referer': self.chapter,
        #     'cookies': self.http().cookies,
        #     'user_agent': self.http().user_agent
        # }).get(self.chapter)
        # parser = self.re.search(r"var\s?imgsrcs\s+?=\s?['\"](.+)['\"]", content)  # TODO: NEED DECRYPT!
        # if not parser:
        #     return []
        # return parser.group(0).split(',')
        pass

    def get_cover(self):
        return self._cover_from_content('#information .cover img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaGoMe
