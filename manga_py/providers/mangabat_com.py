from .manganelo_com import MangaNeloCom


class MangaBatCom(MangaNeloCom):
    __content = None

    def get_main_content(self):
        if self.__content is None:
            return self.http_get(self.get_url())
        return self.__content

    def get_manga_name(self) -> str:
        self.__content = self.http_get(self.get_url())
        return self.text_content(self.__content, 'h1.entry-title')


main = MangaBatCom
