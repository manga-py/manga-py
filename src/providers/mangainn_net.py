from src.provider import Provider


class MangaInnNet(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        groups = self.re.search(r'\.net/[^/]+/([^/]+)', chapter).group(1).split('.')

        idx = [
            groups[0],
            0 if len(groups) < 2 else groups[1]
        ]
        return '{}-{}'.format(*idx)

    def get_main_content(self):
        return self.http_get('{}/{}'.format(self.get_domain(), self.get_manga_name()))

    def get_manga_name(self) -> str:
        name = self.re.search(r'\.net/([^/]+)', self.get_url())
        return name.group(1)

    def get_chapters(self):
        return self.document_fromstring(self.get_storage_content(), '#chapter_list a[href]')

    def get_files(self):
        content = self.http_get(self.get_current_chapter())
        images = self.re.search(r'var\s+images\s*=\s*(\[\{.+?\}\])', content).group(1)
        images = self.json.loads(images)
        return [i.get('url') for i in images]


main = MangaInnNet
