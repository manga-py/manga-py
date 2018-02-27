from src.providers.pecintakomik_com import PecintaKomikCom
from .helpers.std import Std


class PecintaKomikComManga(PecintaKomikCom, Std):

    def get_main_content(self):
        return self._get_content('{}/manga/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'/manga/([^/]+)')

    def get_chapters(self):
        parser = self.document_fromstring(self.get_storage_content())
        items = self._first_select_options(parser, 'select[name="chapter"]', False)
        url = '{}/manga/{}/%s/full'.format(
            self.get_domain(),
            self.get_manga_name()
        )
        return [url % i.get('value') for i in items]

    def get_cover(self) -> str:
        pass


main = PecintaKomikComManga
