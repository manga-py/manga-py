from manga_py.provider import Provider
from .helpers.std import Std


class CycomiCom(Provider, Std):
    @staticmethod
    def remove_not_ascii(value):
        return value

    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return self.chapter[1]

    def __url(self):
        return '{}/fw/cycomibrowser/chapter/title/{}'.format(
            self.domain,
            self.__idx()
        )

    def __idx(self):
        return self.re.search(
            r'/title/(\d+)',
            self.get_url()
        ).group(1)

    def get_main_content(self):
        return self.http_get(self.__url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.title-texts h3')

    def get_chapters(self):
        selector = 'a.chapter-item:not(.is-preread)'
        items = []
        n = self.http().normalize_uri
        for el in self._elements(selector, self.content):
            title = el.cssselect('p.chapter-title')[0]
            title = title.text_content().strip(' \n\r\t\0')
            episode_id = self.re.sub(r'.+pages/(.+)', r'\1', n(el.get('href')))
            title = episode_id + '_' + title
            items.append((n(el.get('href')), title))
        return items

    def get_files(self):
        n = self.http().normalize_uri
        content = self.http_get(self.chapter[0])
        selector = '.comic-image'
        items = self._elements(selector, content)
        return [n(i.get('src')) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.title-image-container img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = CycomiCom
