from manga_py.provider import Provider
from .helpers.std import Std


class MangaLibMe(Provider, Std):

    def get_chapter_index(self) -> str:
        return '{}_{}'.format(
            self.chapter_for_json(),
            self.chapter['chapter_name']
        )

    def get_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.\w{2,7}/([^/]+)')

    def get_chapters(self):
        _json = self.re.search(r'__DATA__\s*=\s*(\{.+?\});', self.content)

        if _json is None:
            return []

        return self.json.loads(_json.group(1)).get('chapters', {}).get('list', [])

    def get_files(self):
        content = self.http_get(self.chapter)
        images = self.re.search(r'__pg\s*=\s*(\[.+\])', content).group(1)
        info = self.re.search(r'__info\s*=\s*(\{.+\})', content).group(1)
        images = self.json.loads(images)
        info = self.json.loads(info)
        _manga = info['img']['url']
        _s = info['servers']
        _server = _s.get('main', _s.get('secondary'))

        return ['{}{}{}'.format(_server, _manga, i['u']) for i in images]

    def get_cover(self):
        return self._cover_from_content('.media-sidebar__cover > img')

    def prepare_cookies(self):
        self.cf_scrape(self.get_url())

    def chapter_for_json(self) -> str:
        return '{}-{}'.format(
            self.chapter['chapter_volume'] or '',
            self.chapter['chapter_number'],
        ).rstrip('-')


main = MangaLibMe
