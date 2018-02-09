from src.provider import Provider


class DesuMe(Provider):

    def get_archive_name(self) -> str:
        idx = self.re.search(r'/vol(\d+)/ch(\d+)', self.get_current_chapter()).groups()
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        result = self.re.search(r'/vol(\d+)/ch(\d+)', self.get_current_chapter()).groups()
        return '{}-{}'.format(result[0], result[1])

    def get_main_content(self):
        name = self.get_manga_name()
        url = '{}/manga/{}'.format(self.get_domain(), name)
        return self.http_get(url)

    def get_chapters(self):
        c, s = self.get_storage_content(), '#animeView ul h4 > a.tips'
        return self.document_fromstring(c, s)

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)', self.get_url()).group(1)

    def get_files(self):
        content = self.http_get(self.get_domain() + self.get_current_chapter())
        result = self.re.search(r'images:\s?(\[\[.+\]\])', content, self.re.M)
        if not result:
            return []
        root_url = self.re.search(r'dir:\s?"([^"]*)"', content).group(1).replace(r'\/', '/')

        return [root_url + i[0] for i in self.json.loads(result.group(1))]


main = DesuMe
