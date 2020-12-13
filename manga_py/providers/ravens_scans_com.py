from .gomanga_co import GoMangaCo
from .helpers.std import Std


class RavensScansCom(GoMangaCo, Std):
    _name_re = '/(?:serie|read)/([^/]+)'
    __api_url = '/lector/api/v2/comic?stub='

    def get_content(self):
        url = '{}{}{}'.format(self.domain, self.__api_url, self.manga_name)
        return self.json.loads(self.http_get(url)).get('languages', [])

    def get_chapters(self):
        items = []
        for i in self.content:
            url = '{}{}{}&lang={}'.format(self.domain, self.__api_url, self.manga_name, i)
            items += self.json.loads(self.http_get(url)).get('chapters', [])
        return [i.get('href') for i in items[::-1]]  # DON'T TOUCH THIS!

    def get_cover(self) -> str:
        return self.content.get('fullsized_thumb_url', None)


main = RavensScansCom
