import re

from lxml.html import document_fromstring

from libs.fs import basename


class BaseProvider:
    _storage = {
        'cookies': (),
        'main_content': '',
        'chapters': [],
        'current_chapter': 0,
        'current_file': 0
    }
    _params = {
        'path_destination': 'Manga'
    }

    @staticmethod
    def document_fromstring(body, selector: str = None, idx: int = None):
        result = document_fromstring(body)
        if isinstance(selector, str):
            result = result.cssselect(selector)
        if isinstance(idx, int):
            result = result[abs(idx)]
        return result

    @staticmethod
    def _set_if_not_none(var, key, value):
        if value is not None:
            var[key] = value

    @staticmethod
    def re_match(pattern, string, flags=0):
        return re.match(pattern, string, flags)

    @staticmethod
    def re_search(pattern, string, flags=0):
        return re.search(pattern, string, flags)

    @staticmethod
    def basename(_path) -> str:
        return basename(_path)

    def get_url(self):
        return self._params['url']

    def get_domain(self):
        domain_uri = self._params.get('domain_uri', None)
        if not domain_uri:
            self._params['domain_uri'] = re.search('(https?://[^/]+)', self._params['url']).group(1)

        return self._params['domain_uri']

    def get_current_chapter(self):
        return self._storage['chapters'][self._storage['current_chapter']]

    def get_current_file(self):
        return self._storage['files'][self._storage['current_file']]

    def quest_callback(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        pass

    def files_progress_callback(self, max_val: int, current_val: int, need_reset=False):
        pass

    def logger_callback(self, *args):
        pass

    def get_referrer(self):
        return self.referrer if hasattr(self, 'referrer') else self.get_domain()
