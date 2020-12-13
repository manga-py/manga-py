from manga_py.provider import Provider
from .helpers.std import Std


class MangaTubeMe(Provider, Std):

    def get_chapter_index(self) -> str:
        txt = self.chapter[0].strip()
        idx = self.re.search(r'.*?(\d+(?:\.\d+)?)', txt)
        if not idx:
            return str(self.chapter_id)
        return idx.group(1).replace('.', '-')

    def get_content(self):
        return self._get_content('{}/series/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/series/([^/]+)/')

    def get_chapters(self):
        items = self._elements('#chapter li > a')
        return [(i.text_content(), i.get('href')) for i in items]

    def get_files(self):
        n = self.http().normalize_uri
        content = self.http_get(n(self.chapter[1]))
        img_path = self.re.search(r'img_path[\'"]?:\s[\'"](.+)[\'"]', content)
        img_path = n(img_path.group(1))
        images = self.re.search(r'pages[\'"]?:\s(\[\{.+\}\])', content)
        images = self.json.loads(images.group(1))
        return ['{}{}'.format(img_path, i.get('file_name')) for i in images]

    def get_cover(self):
        return self._cover_from_content('.owl-carousel img', 'data-original')

    def book_meta(self) -> dict:
        # todo meta
        pass

    def chapter_for_json(self):
        return self.chapter[1]


main = MangaTubeMe
