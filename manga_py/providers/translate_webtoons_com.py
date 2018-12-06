from manga_py.provider import Provider
from .helpers.std import Std


class TranslateWebToonsCom(Provider, Std):
    def get_archive_name(self) -> str:
        return self.normal_arc_name(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return self.re.search(r'\bepisodeNo=(\d+)', self.chapter).group(1)

    def get_main_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, 'h3.subj')

    def _chapters(self, content):
        return self._elements('.detail_lst > ul > li > a', content)

    @staticmethod
    def _filter_chapters(chapters):
        result = []
        for item in chapters:
            content = item.cssselect('.rate_num.cplt')[0].text_content().strip('\n\t\r \0')
            if content == '100%':
                result.append(item)
        return result

    def get_chapters(self):
        pages = self._elements('.paginate > a:not([class])')
        chapters = self._chapters(self.content)
        if pages:
            n = self.http().normalize_uri
            for i in pages:
                content = self.http_get(n(i.get('href')))
                chapters += self._chapters(content)
        return self._filter_chapters(chapters)

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, '.img_info > img')

    def get_cover(self) -> str:
        return self._cover_from_content('.thmb img')

    def book_meta(self) -> dict:
        # todo meta
        pass


main = TranslateWebToonsCom
