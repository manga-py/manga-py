from .manganelo_com import MangaNeloCom


class MangaBatCom(MangaNeloCom):
    def get_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.story-info-right h1')

    def prepare_cookies(self):
        if not ~self.get_url().find(self._prefix):
            self._prefix = '/'

        super().prepare_cookies()


main = MangaBatCom
