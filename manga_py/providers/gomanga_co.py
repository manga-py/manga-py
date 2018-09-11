from manga_py.provider import Provider
from .helpers.std import Std


class GoMangaCo(Provider, Std):
    _name_re = '/reader/[^/]+/([^/]+)/'
    _content_str = '{}/reader/series/{}/'
    _chapters_selector = '.list .element .title a'

    def get_chapter_index(self) -> str:
        url = self.chapter
        index_re = r'/rea\w+/[^/]+/[^/]+/(?:[^/]+/)?(\d+/\d+(?:/\d+)?)'
        group = self.re.search(index_re, url).group(1)
        return group.replace('/', '-')

    def get_main_content(self):
        return self._get_content(self._content_str)

    def get_manga_name(self) -> str:
        return self._get_name(self._name_re)

    def get_chapters(self):
        return self._elements(self._chapters_selector)

    def _get_json_selector(self, content):
        idx = self.re.search(r'page_width\s=\sparseInt\((\w+)\[', content).group(1)
        return r'var\s{}\s*=\s*(\[.+\])'.format(idx)

    def get_files(self):
        content = self.http_get(self.chapter)
        selector = self._get_json_selector(content)
        items = self.json.loads(self.re.search(selector, content).group(1))
        return [i.get('url') for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.cover img')

    def prepare_cookies(self):
        url = self.get_url()
        self.cf_protect(url)
        data = {'adult': 'true'}
        try:
            response = self.http().requests(method='post', data=data, url=url)
            cookies = response.cookies.items()
            for i in cookies:
                self._storage['cookies'][i[0]] = i[1]
        except Exception:
            pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = GoMangaCo
