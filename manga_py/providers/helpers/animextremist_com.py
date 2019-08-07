from manga_py.provider import Provider


class AnimeXtremistCom:
    provider = None
    path = None

    def __init__(self, provider: Provider):
        self.provider = provider
        self.path = provider.get_url()

    @staticmethod
    def build_path(item):
        return item[0] + item[1]

    @staticmethod
    def __sort(item, selector):
        _re = selector.search(item)
        if _re:
            return int(_re.group(1))
        return 0

    def sort_items(self, items):
        r = self.provider.re.compile(r'.+?-(\d+)')
        return sorted(items, key=lambda i: self.__sort(i[0], r))

    def sort_images(self, items):
        r = self.provider.re.compile(r'.+/.+-(\d+)[^/]*\.html')
        return sorted(items, key=lambda i: self.__sort(i, r))

    def _chapters(self, url=None):
        a = 'li + li > a'
        if url:
            items = self.provider.html_fromstring(url, a)
        else:
            items = self.provider.document_fromstring(self.provider.content, a)
        return items

    # http://animextremist.com/mangas-online/99love/
    def _chapters_with_dirs(self, items):
        result = []
        for i in items:
            href = i.get('href')
            url = '{}{}'.format(self.path, href)
            result += [(href, ['{}{}'.format(
                url,
                a.get('href')
            ) for a in self._chapters(url)])]
        return result

    @staticmethod
    def _rebuild_dict_to_tuple(_dict):
        result = []
        for i in _dict:
            result += [(i, [a for a in _dict[i]])]
        return result

    # http://animextremist.com/mangas-online/onepiece-manga/
    def _chapters_without_dirs(self, items):
        result = {}
        r = self.provider.re.compile(r'(.+?-\d+)')  # todo
        for i in items:
            href = i.get('href')
            key = self.provider.re.search(r, href).group(1)
            if result.get(key) is None:
                result[key] = []
            result[key].append('{}{}'.format(self.path, href))
        return self._rebuild_dict_to_tuple(result)

    def get_chapters(self):
        items = self._chapters()
        if len(items) and items[0].get('href').find('.html') < 0:
            items = self._chapters_with_dirs(items)
        else:
            items = self._chapters_without_dirs(items)
        return self.sort_items(items)

    def get_page_image(self, src, selector, attr='src') -> str:
        image = self.provider.html_fromstring(src, selector)
        if image and len(image):
            return image[0].get(attr)
