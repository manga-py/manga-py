from .rawdevart_com_old import RawDevArtComOld
from requests import get


class HiperDexCom(RawDevArtComOld):
    _chapter_selector = r'/manga/[^/]+/(?:chapter-)?(\d+(?:[\.-]\d+)?)/'

    def get_chapters(self):
        manga_id = self.document_fromstring(self.content, '#manga-chapters-holder', 0).get('data-id')
        content = self.http_post('{}/wp-admin/admin-ajax.php'.format(self.domain), data={
            'action': 'manga_get_chapters',
            'manga': manga_id,
        })

        return self._elements('.wp-manga-chapter > a', content)

    def _downloader(self, url, file_name):
        with open(str(file_name), 'wb') as w:
            w.write(get(url).content)
        return True

    def prepare_cookies(self):
        self.http()._safe_downloader = self._downloader
        self.http().referer = self.get_url()


main = HiperDexCom
