from manga_py.provider import Provider
from .helpers.std import Std
from .helpers.manganelo_com_helper import check_alternative_server


class MangaKakalotCom(Provider, Std):
    # __alternative_cdn = 'https://bu2.mkklcdnbuv1.com'

    def get_chapter_index(self) -> str:
        re = self.re.search('/chapter_([^/]+)', self.chapter)
        return re.group(1).replace('.', '-', 2)

    def get_content(self):
        return self.http_get(self.get_url())

    def __new_url(self):
        from requests import get
        from sys import stderr
        with get(self.get_url()) as req:
            if req.url != self.get_url():
                print('New url: %s' % req.url, file=stderr)

            self._params['url'] = req.url
            self._storage['main_content'] = req.text

    def get_manga_name(self) -> str:
        if ~self.get_url().find('/manga/'):
            self.__new_url()

        return self._get_name(r'/(?:read-|manga/)(\w+)')

    def get_chapters(self):
        return self._elements('.chapter-list span a')

    def get_files(self):
        chapter = self.chapter
        result = self.html_fromstring(chapter, '#vungdoc img, .container-chapter-reader > img')
        images = [i.get('src') for i in result]
        return images
        # check_alternative_server(images, self.__alternative_cdn, headers={
        #     'Referer': chapter,
        #     'Accept': 'image/webp,*/*',
        # })

    def book_meta(self) -> dict:
        # todo meta
        pass


main = MangaKakalotCom
