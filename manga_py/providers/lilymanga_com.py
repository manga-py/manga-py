from .rawdevart_com_old import RawDevArtComOld


class LilyMangaCom(RawDevArtComOld):
    def get_chapter_index(self) -> str:
        return self.re.search(r'/(?:episode|chapter)-(\d+(?:-\d+)?)', self.chapter).group(1)

    def get_content(self):
        return self._get_content('{domain}/ys/{manga_name}/', manga_name=self._name())

    def get_manga_name(self) -> str:
        return self._name().replace('-', ' ')

    def get_chapters(self):
        manga_id = self._elements('#manga-chapters-holder')[0].get('data-id')
        items_content = self.http().post('{}/wp-admin/admin-ajax.php'.format(self.domain), data={
            'action': 'manga_get_chapters',
            'manga': manga_id,
        }).text

        return self._elements('.wp-manga-chapter > a', items_content)

    def _name(self):
        return self._get_name('/ys/([^/]+)')


main = LilyMangaCom
