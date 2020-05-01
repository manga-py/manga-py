from .rawdevart_com import RawDevArtCom


class HiperDexCom(RawDevArtCom):
    _chapter_selector = r'/manga/[^/]+/(\d+(?:\.\d+)?)/'

    def get_chapters(self):
        manga_id = self.document_fromstring(self.content, '#manga-chapters-holder', 0).get('data-id')
        content = self.http_post('{}/wp-admin/admin-ajax.php'.format(self.domain), data={
            'action': 'manga_get_chapters',
            'manga': manga_id,
        })

        return self._elements('.wp-manga-chapter > a', content)


main = HiperDexCom
