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
    def _first_select_options(parser, selector, skip_first=True) -> list:
        options = 'option'
        if skip_first:
            options = 'option + option'
        select = parser.cssselect(selector)
        if select:
            return select[0].cssselect(options)
        return []

    @classmethod
    def _images_helper(cls, parser, selector, attr='src') -> list:
        image = parser.cssselect(selector)
        return [i.get(attr).strip(r' \r\n\t\0') for i in image]

    @classmethod
    def _idx_to_x2(cls, idx, default=0) -> list:
        return [
            str(idx[0]),
            str(default if len(idx) < 2 or not idx[1] else idx[1])
        ]

    @staticmethod
    def _join_groups(idx, glue='-') -> str:
        result = []
        for i in idx:
            if i:
                result.append(i)
        return glue.join(result)

    def _get_name(self, selector, url=None) -> str:
        if url is None:
            url = self.get_url()
        return self.re.search(selector, url).group(1)

    def _get_content(self, selector) -> str:
        return self.http_get(selector.format(self.domain, self.manga_name))

    def _base_cookies(self):
        cookies = self.http().get_base_cookies(self.get_url())
        self._storage['cookies'] = cookies.get_dict()

    def parse_background(self, image) -> str:
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

    @staticmethod
    def normal_arc_name(idx):
        fmt = 'vol_{:0>3}'
        if len(idx) > 1:
            fmt += '-{}'
        return fmt.format(*idx)


class Http2:
    provider = None
    path_join = None
    is_file = None

    def __init__(self, provider):
        from manga_py.fs import path_join, is_file
        self.provider = provider
        self.path_join = path_join
        self.is_file = is_file

    def _get_name(self, url):
        archive = self.provider._params.get('name', '')
        if not len(archive):
            archive = self.provider._storage['manga_name']
        return self.path_join(
            self.provider._params.get('path_destination', 'Manga'),
            archive,
            url[0]
        )

    def download_archives(self):
        volumes = self.provider._storage['chapters']
        _min = self.provider._params.get('skip_volumes', 0)
        _max = _min + self.provider._params.get('max_volumes', 0)
        for idx, url in enumerate(volumes):
            self.provider._storage['current_chapter'] = idx
            name = self._get_name(url)
            if idx < _min or (idx > _max > 0) or self.is_file(name):
                continue
            self.provider.http().download_file(url[1], name)
