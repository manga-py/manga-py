from ._http2 import Http2


class Std:
    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return self.normal_arc_name({'vol': idx.split('-')})

    def _elements(self, selector, content=None) -> list:
        if not content:
            content = self.content
        return self.document_fromstring(content, selector)

    def _cover_from_content(self, selector, attr='src') -> str:
        image = self._elements(selector)
        if image is not None and len(image):
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
        return [i.get(attr).strip(' \r\n\t\0') for i in image]

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

    def _base_cookies(self, url=None):
        if url is None:
            url = self.get_url()
        cookies = self.http().get_base_cookies(url)
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

    def normal_arc_name(self, idx):
        if isinstance(idx, str):
            idx = [idx]
        if isinstance(idx, list):
            return self.__normal_name_list(idx)
        if isinstance(idx, dict):
            return self.__normal_name_dict(idx)
        raise DeprecationWarning('Wrong arc name type: %s' % type(idx))

    @staticmethod
    def __fill(var, fmt: str = '-{}'):
        if isinstance(var, str):
            var = [var]
        return (fmt * len(var)).format(*var).lstrip('-')

    def __normal_name_list(self, idx: list):
        fmt = 'vol_{:0>3}'
        if len(idx) > 1:
            fmt += '-{}' * (len(idx) - 1)
        if self._zero_fill and len(idx) < 2:
            idx.append('0')
            fmt += '-{}'
        return fmt.format(*idx)

    def __normal_name_dict(self, idx: dict):
        vol = idx.get('vol', ['0'])
        ch = idx.get('ch', None)
        fmt = 'vol_{:0>3}'
        data = [vol[0]]
        if len(vol) > 1:
            fmt += '-{}'
            del vol[0]
            data += [self.__fill(vol, '-{}')]
        elif self._zero_fill:
            fmt += '-{}'
            data += ['0']
        if ch:
            fmt += '-ch_{}'
            data.append(self.__fill(ch))
        result = fmt.format(*data)
        if self._with_manga_name:
            result = '%s-%s' % (self.manga_name, result)
        return result

    def text_content(self, content, selector, idx: int = 0, strip: bool = True):
        doc = self.document_fromstring(content, selector)
        if not doc:
            return None
        text = doc[idx].text_content()
        if strip:
            text = text.strip()
        return text
