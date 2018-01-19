from .provider import Provider


class JurnaluRu(Provider):

    def get_archive_name(self) -> str:
        name = self.get_manga_name()
        arc_name = self.re.search('/{0}/{0}([^/]+)'.format(name), self.get_current_chapter())
        if arc_name:
            pass
        return 'chapter_{}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        return str(self._storage['current_chapter'])

    def get_main_content(self):
        name = self.re.search('(online\\-reading/[^/]+/[^/]+)', self.get_url()).group(1)
        url = self.html_fromstring(
            '{}/{}'.format(self.get_domain(), name),
            '.MagList .MagListLine > a',
            0
        ).get('href')
        return self.http_get(self.get_domain() + url)

    def get_manga_name(self) -> str:
        return self.re.search('/online\\-reading/[^/]+/([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        name = self.re.search('(online\-reading/[^/]+/[^/]+)', self.get_url())
        if not name:
            return []
        items = self.document_fromstring(self.get_main_content(), 'select.magSelection option')
        url = '{}/{}/'.format(self.get_domain(), name.group(1))
        return [url + i.get('value') for i in items]

    def prepare_cookies(self):
        pass

    @staticmethod
    def __get_file(parser):
        image = parser.cssselect('a[rel="shadowbox"]')
        return image[0].get('href')

    def get_files(self):
        chapter = self.get_current_chapter()
        page = self.html_fromstring(chapter, '.ForRead', 0)
        pages = page.cssselect('.navigation')[0].cssselect('select.M option + option')
        images = [self.__get_file(page)]
        for i in pages:
            uri = '{}/{}'.format(chapter, i.get('value'))
            parser = self.html_fromstring(uri, '.ForRead', 0)
            images.append(self.__get_file(parser))
        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = JurnaluRu
