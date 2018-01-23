from .provider import Provider


class ReadmangaMe(Provider):

    def get_archive_name(self):
        name = self.re.search('/.+/([^/]+/[^/]+)/?', self.get_current_chapter())
        return name.group(1).replace('/', '-')

    def get_main_content(self):
        url = '{}/{}?mature=1&mtr=1'.format(self.get_domain(), self.get_manga_name())
        return self.http_get(url)

    def get_manga_name(self):
        return self.re.search('\\.me/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        parser = self.document_fromstring(self.get_main_content(), 'div.chapters-link tr > td > a')
        if not parser:
            return []
        return [i.get('href') for i in parser]

    def prepare_cookies(self):
        pass

    def get_files(self):
        _uri = self.http().normalize_uri(self.get_current_chapter())
        content = self.http_get(_uri)
        result = self.re.search('rm_h\\.init.+?(\[\[.+\]\])', content, self.re.M)
        if not result:
            return []
        return [i[1] + i[0] + i[2] for i in self.json.loads(result.groups()[0].replace("'", '"'))]

    def get_chapter_index(self):
        name = self.re.search('/.+/(?:vol)?([^/]+/[^/]+)/?', self.get_current_chapter())
        return name.group(1).replace('/', '-')

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = ReadmangaMe
