from urllib.parse import urlparse, urljoin, ParseResult


class Normalize:
    _base = None

    def __init__(self, base):
        self._base = urlparse(base)

    def get_fragment(self, fragment: str, _base: ParseResult = None) -> str:
        """
        :param fragment: Allowed:
            'fragment', 'hostname', 'netloc',
            'params', 'password', 'path',
            'port', 'query', 'scheme', 'username'
        :param _base: ParseResult
        :return:
        """
        if _base is None:
            _base = self._base
        return getattr(_base, fragment)

    def restore(self, url: str) -> str:
        """
        :param url:
        :return:
        """
        _restored = urlparse(url)
        scheme, netloc, path = self.__restore_path(self._base, _restored)
        return '%s://%s%s' % (scheme, netloc, path)

    @staticmethod
    def __restore(_base: ParseResult, _url: ParseResult, fragment) -> str:
        attr = getattr(_url, fragment, None)
        if attr is None or len(attr) == 0:
            return getattr(_base, fragment, None)
        return attr

    def __restore_path(self, _base: ParseResult, _restored: ParseResult) -> tuple:
        _scheme = self.__restore(self._base, _restored, 'scheme')
        _netloc = self.__restore(self._base, _restored, 'netloc')
        scheme, netloc, path = _restored.scheme, _restored.netloc, _restored.path
        if scheme or netloc:  # //a.org, http:///a.html
            return _scheme, _netloc, path
        else:
            path = urljoin('%s://%s%s' % (scheme, netloc, _base.path), path)
            return _scheme, _netloc, path


__cache = {}


def normalize(restore_url: str, base: str = None):
    if base is None:
        __cache['last'] = Normalize(base)
    return __cache['last'].restore(restore_url)
