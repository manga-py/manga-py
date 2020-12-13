from manga_py.provider import Provider
from .helpers.std import Std


class ReadmangaMe(Provider, Std):
    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        vol, ch = idx.split('-')
        return self.normal_arc_name({'vol': vol, 'ch': ch})

    def get_chapter_index(self):
        _re = r'/.+/(?:vol)?([^/]+/[^/]+)(?:/|\?ma?t)?'
        name = self.re.search(_re, self.chapter).group(1)
        if ~name.find('?'):
            name = name[:name.find('?')]
        return name.replace('/', '-')

    def get_content(self):
        return self._get_content('{}/{}?mature=1&mtr=1')

    def get_manga_name(self):
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        return self._elements('div.chapters-link tr > td > a')

    def get_files(self):
        _uri = self.http().normalize_uri(self.chapter)
        content = self.http_get(_uri)
        result = self.re.search(r'rm_h\.init.+?(\[\[.+\]\])', content, self.re.M)
        if not result:
            return []
        images = self.json.loads(
            result.groups()[0].replace("'", '"')
        )
        return [i[0] + i[2] for i in images]

    def get_cover(self):
        return self._cover_from_content('.picture-fotorama > img')


main = ReadmangaMe
