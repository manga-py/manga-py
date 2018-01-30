from libs.provider import Provider


class DesuMe(Provider):

    def get_archive_name(self) -> str:
        return self.re_search('/(vol\\d+/ch\\d+)', self.get_current_chapter()).group(1).replace('/', '_')

    def get_chapter_index(self) -> str:
        result = self.re_search('/vol(\\d+)/ch(\\d+)', self.get_current_chapter()).groups()
        return '{}-{}'.format(result[0], result[1])

    def get_main_content(self):
        name = self.get_manga_name()
        url = '{}/manga/{}'.format(self.get_domain(), name)
        return self.http_get(url)

    def get_chapters(self):
        parser = self.document_fromstring(self.get_storage_content(), '#animeView ul h4 > a.tips')
        return [i.get('href') for i in parser]

    def get_manga_name(self) -> str:
        return self.re_search('/manga/([^/]+)', self.get_url()).group(1)

    def prepare_cookies(self):
        pass

    def get_files(self):
        content = self.http_get(self.get_domain() + self.get_current_chapter())
        result = self.re_search('images:\\s?(\\[\[.+\\]\\])', content, self.re.M)
        if not result:
            return []
        root_url = self.re_search('dir:\\s?"([^"]*)"', content).group(1).replace('\\/', '/')

        return [root_url + i[0] for i in self.json.loads(result.group(1))]

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = DesuMe
