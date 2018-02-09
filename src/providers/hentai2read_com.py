from src.provider import Provider


class Hentai2ReadCom(Provider):
    images_cdn = 'https://static.hentaicdn.com/hentai'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(
            idx[0],
            0 if len(idx) < 2 else idx[1]
        )

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        idx = self.re.search('.+/([^/]+)/', chapter)
        return '-'.join(idx.group(1).split('.'))

    def get_main_content(self):
        return self.http_get('{}/{}/'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        return self.re.search(r'\.com/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        c, s = self.get_storage_content(), 'li .chapter-row'
        return self.document_fromstring(c, s)

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        selector = r'\'images\'\s*:\s*(\[.+\])'
        items = self.json.loads(self.re.search(selector, content).group(1))
        return ['{}{}'.format(self.images_cdn, i) for i in items]

    def get_cover(self) -> str:
        return self._get_cover_from_content('.ribbon-primary .border-black-op')


main = Hentai2ReadCom
