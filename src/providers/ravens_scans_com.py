from src.providers.gomanga_co import GoMangaCo
from .helpers.std import Std


class RavensScansCom(GoMangaCo, Std):
    _name_re = '/(?:serie|read)/([^/]+)'
    __api_url = '/lector/api/v2/comic?stub='

    def get_main_content(self):
        name = self.get_manga_name()
        url = '{}{}{}'.format(self.get_domain(), self.__api_url, name)
        return self.json.loads(self.http_get(url)).get('languages', [])

    def get_chapters(self):
        langs = self.get_storage_content()
        items = []
        for i in langs:
            name = self.get_manga_name()
            url = '{}{}{}&lang={}'.format(self.get_domain(), self.__api_url, name, i)
            items += self.json.loads(self.http_get(url)).get('chapters', [])
        return [i.get('href') for i in items[::-1]]  # DON'T TOUCH THIS!

    def get_cover(self) -> str:
        content = self.get_storage_content()
        return content.get('fullsized_thumb_url', None)


main = RavensScansCom
