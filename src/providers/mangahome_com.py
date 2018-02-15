from src.provider import Provider
from .helpers.std import Std


class MangaHomeCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{}-{}'.format(*self._idx_to_x2(idx))

    def get_chapter_index(self) -> str:
        selector = r'/manga/[^/]+/[^\d]+(\d+)(?:\.(\d+))?'
        idx = self.re.search(selector, self.get_current_chapter()).groups()
        return self._join_groups(idx)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        return self._chapters('.detail-chlist a')

    def get_files(self):
        img_selector = 'img#image'
        _url = self.http().normalize_uri(self.get_current_chapter())
        parser = self.html_fromstring(_url)
        pages_selector = '.mangaread-top .mangaread-pagenav select option + option'
        pages = [i.get('value') for i in parser.cssselect(pages_selector)]

        images = self._images_helper(parser, img_selector)

        for i in pages:
            url = self.http().normalize_uri(i)
            images += self._images_helper(parser, img_selector)

        return images


main = MangaHomeCom
