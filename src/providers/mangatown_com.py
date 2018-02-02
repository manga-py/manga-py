from src.provider import Provider


class MangaTownCom(Provider):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        idx = self.re_search('/manga/[^/]+/c([^/]+)', self.get_current_chapter())
        idx = idx.group(1).split('.')
        return '{}-{}'.format(
            idx[0],
            0 if len(idx) < 2 else idx[1]
        )

    def get_main_content(self):
        name = self.get_manga_name()
        url = '{}/manga/{}/'.format(self.get_domain(), name)
        return self.http_get(self.http().normalize_uri(url))

    def get_manga_name(self) -> str:
        return self.re_search('/manga/([^/]+)/?', self.get_url()).group(1)

    def get_chapters(self):
        items = self.document_fromstring(self.get_storage_content(), '.chapter_list a')
        return [i.get('href') for i in items]

    def prepare_cookies(self):
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._http_kwargs['verify'] = False

    def get_files(self):
        url = self.http().normalize_uri(self.get_current_chapter())
        parser = self.html_fromstring(url)
        selector = '#top_chapter_list + .page_select select option + option'
        images = [parser.cssselect('img#image')[0].get('src')]

        for i in parser.cssselect(selector):
            url = self.http().normalize_uri(i.get('value'))
            img = self.html_fromstring(url, 'img#image')
            len(img) and images.append(img[0].get('src'))

        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = MangaTownCom
