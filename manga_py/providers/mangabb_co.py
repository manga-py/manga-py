from manga_py.provider import Provider
from .helpers.std import Std


class MangabbCo(Provider, Std):

    def get_chapter_index(self) -> str:
        chapter = self.chapter
        idx = chapter.rfind('/chapter-')
        return chapter[1 + idx:]

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.co/(?:manga/)?([^/]+)')

    def get_chapters(self):
        content = self.document_fromstring(self.content, '#chapters a')
        if not content:
            return []
        selector = '#asset_1 select.chapter_select > option'
        result = self.html_fromstring(content, selector)
        return [i.get('value') for i in result[::-1]]

    @staticmethod
    def __get_img(parser):
        return parser.cssselect('#manga_viewer > a > img')[0].get('src')

    @staticmethod
    def _img_lifehack1(img, pages_list, images):
        n = 1
        for i in pages_list:
            n += 1
            images.append('{}{}{}'.format(img[0], n, img[1]))

    def _img_lifehack2(self, pages_list, images):
        for page in pages_list:
            parser = self.html_fromstring(page)
            images.append(self.__get_img(parser))

    def get_files(self):
        parser = self.html_fromstring(self.chapter, '#body', 0)
        result = parser.cssselect('#asset_2 select.page_select option + option')
        pages_list = [i.get('value') for i in result]
        _first_image = self.__get_img(parser)
        images = [_first_image]

        img = self.re.search(r'(.+/)\d(\.\w+)', _first_image)
        if img:  # livehack
            self._img_lifehack1(img.groups(), pages_list, images)
        else:
            self._img_lifehack2(pages_list, images)

        return images

    def get_cover(self):
        return self._cover_from_content('#series_image')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangabbCo
