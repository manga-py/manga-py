from src.provider import Provider
# from re import search


class AnimeXtremistCom:
    provider = None
    path = None

    def __init__(self, provider: Provider):
        self.provider = provider
        self.path = provider.get_manga_url()

    @staticmethod
    def build_path(item):
        return item[0] + item[1]

    def sort_items(self, items):
        re = self.provider.re.search
        return sorted(items, key=lambda item: re(r'.+?-(\d+)', item[0]).group(1))

    @staticmethod
    def _check_key(obj, key):
        if key not in obj.keys():
            obj[key] = []

    def _chapters(self, url=None):
        a = 'li + li > a'
        if url:
            print(url)
            items = self.provider.html_fromstring(url, a)
        else:
            items = self.provider.document_fromstring(self.provider.get_storage_content(), a)
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
    def _chapters_without_dirs(self, items):  # very slowly function
        result = {}
        for i in items:
            href = i.get('href')
            key = self.provider.re.search(r'(.+?-\d+)', href).group(1)
            self._check_key(result, key)
            result[key].append('{}{}'.format(self.path, href))
        return self._rebuild_dict_to_tuple(result)

    def get_chapters(self):
        items = self._chapters()
        if len(items) and items[0].get('href').find('.html') < 0:
            items = self._chapters_with_dirs(items)
        else:
            items = self._chapters_without_dirs(items)
        # items = [('dir/', 'capitulo-1.html')]
        # items = [('', 'capitulo-1-1.html')]
        print('get_chapters')
        print(self.sort_items(items))
        exit()
        return self.sort_items(items)
