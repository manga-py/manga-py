from manga_py.provider import Provider
from .helpers.std import Std


class MangaFoxMe(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        selector = '/manga/[^/]+/([^/]+)/'
        chapter = self.chapter
        idx = self.re.search(selector, chapter).group(1).split('.')
        return '{}-{}'.format(*self._idx_to_x2(idx))

    def get_main_content(self):
        return self._get_content('{}/manga/{}')

    def get_manga_name(self) -> str:
        return self._get_name('/manga/([^/]+)/?')

    def get_chapters(self):
        return self._elements('#chapters a.tips')

    def __get_files_url(self):
        volume = self.chapter
        url = self.http().normalize_uri(volume)
        if ~url.find('.html'):
            url = url[: url.rfind('/')]
        return url

    def get_files(self):
        img_selector = 'img#image'
        _url = self.__get_files_url()
        url = '{}/1.html'.format(_url)
        selector = '#top_bar .r .l select.m option'
        parser = self.html_fromstring(url)
        pages = [i.get('value') for i in parser.cssselect(selector)]

        images = self._images_helper(parser, img_selector)

        for n in pages:
            if int(n) < 2:
                continue
            url = '{}/{}.html'.format(_url, n)
            parser = self.html_fromstring(url)
            images += self._images_helper(parser, img_selector)

        return images

    def get_cover(self):
        pass  # TODO


main = MangaFoxMe
