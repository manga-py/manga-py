# All providers

### For template example, see _template.py

## Functions:

```python
from manga_py.provider import Provider
# from .helpers.std import Std


class _Template(Provider):
# class _Template(Provider, Std):  # extends utils

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):  # call once
#       return self._get_content('{}/manga/{}')
        pass

    def prepare_cookies(self):  # if site with cookie protect
#        self._storage['proxies'] = auto_proxy()

#        self._storage['cookies'] = self.http().get_base_cookies(self.get_url()).get_dict()  # base cookies
        pass

    def get_manga_name(self) -> str:
#       return self._get_name('/manga/([^/]+)')
        return ''

    def get_chapters(self):  # call once
        # return self._elements('a.chapter')
        return []

    def get_files(self):  # call ever volume loop
        return []

    def get_cover(self) -> str:
        # return self._cover_from_content('.cover img')
        pass

    def book_meta(self) -> dict: 
        """
        :see http://acbf.wikia.com/wiki/Meta-data_Section_Definition
        :return  {
            'author': str,
            'title': str,
            'genre': list('manga', 'real_life',),
            'annotation': str,
            'keywords': str,
            'cover': str,
            'rating': str,
          }
        """
        pass


main = _Template

```