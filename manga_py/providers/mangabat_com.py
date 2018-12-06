from .manganelo_com import MangaNeloCom


class MangaBatCom(MangaNeloCom):
    def get_main_content(self):
        return self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, 'h1.entry-title')


main = MangaBatCom
