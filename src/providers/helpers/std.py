class Std:
    def _elements(self, idx, content=None) -> list:
        if not content:
            content = self.content
        return self.document_fromstring(content, idx)

    def _cover_from_content(self, selector, attr='src') -> str:
        image = self._elements(selector)
        if image and len(image):
            return self.http().normalize_uri(image[0].get(attr))

    @staticmethod
    def _first_select_options(parser, selector, skip_first=True):
        options = 'option'
        if skip_first:
            options = 'option + option'
        select = parser.cssselect(selector)
        if select:
            return select[0].cssselect(options)
        return []

    @classmethod
    def _images_helper(cls, parser, selector, attr='src'):
        image = parser.cssselect(selector)
        return [i.get(attr).strip(r' \r\n') for i in image]

    @classmethod
    def _idx_to_x2(cls, idx, default=0) -> list:
        return [
            str(idx[0]),
            str(default if len(idx) < 2 or not idx[1] else idx[1])
        ]

    @staticmethod
    def _join_groups(idx, glue='-'):
        result = ''
        for n, i in enumerate(idx):
            if i is not None and i != '':
                if n > 0:
                    result += glue
                result += '{}'.format(i)
        return result

    def _get_name(self, selector):
        return self.re.search(selector, self.get_url()).group(1)

    def _get_content(self, selector):
        return self.http_get(selector.format(self.domain, self.manga_name))

    def _base_cookies(self):
        cookies = self.http().get_base_cookies(self.get_url())
        self._storage['cookies'] = cookies.get_dict()

    def parse_background(self, image):
        selector = r'background.+?url\([\'"]?([^\s]+?)[\'"]?\)'
        url = self.re.search(selector, image.get('style'))
        return self.http().normalize_uri(url.group(1))

    @property
    def content(self):
        content = self._storage.get('main_content', None)
        if content is None:
            content = self.get_main_content()
        return content

    @property
    def manga_name(self) -> str:
        name = self._storage.get('manga_name', None)
        if name is None:
            name = self.get_manga_name()
        return name

    @property
    def domain(self) -> str:
        domain = self._storage.get('domain_uri', None)
        if domain is None:
            domain = self.get_domain()
        return domain

    @property
    def chapter(self) -> str:
        return self.get_current_chapter()
