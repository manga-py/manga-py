from urllib.parse import urlparse

from src.fs import remove_file_query_params, path_join


class UrlNormalizer:

    @staticmethod
    def _parse_sheme(parse, base_parse):
        if not parse.scheme:
            uri = base_parse.scheme
        else:
            uri = parse.scheme
        return uri + '://'

    @staticmethod
    def _parse_netloc(parse, base_parse):
        if not parse.netloc:
            uri = base_parse.netloc
        else:
            uri = parse.netloc
        return uri

    @staticmethod
    def _test_path_netloc(parse):
        if parse.path.find('://') == 0:
            return urlparse('http' + parse.path).path
        return parse.path

    @staticmethod
    def __parse_rel_path(parse, base_parse):
        path = ''
        if base_parse.path.rfind('/') > 0:
            path = base_parse.path[0:base_parse.path.rfind('/')]
        return path.rstrip('/') + '/' + parse.path.lstrip('/')

    @staticmethod
    def _parse_path(parse, base_parse):
        _path = UrlNormalizer._test_path_netloc(parse)
        if _path:
            if _path.find('/') == 0:
                return _path
            else:
                return UrlNormalizer.__parse_rel_path(parse, base_parse)
        else:
            return base_parse.path

    @staticmethod
    def _parse_query(parse):
        if parse.query:
            return '?' + parse.query
        return ''

    @staticmethod
    def _parse_fragment(parse):
        if parse.fragment:
            return '#' + parse.fragment
        return ''

    @staticmethod
    def url_helper(url: str, base_url: str) -> str:
        parse = urlparse(url)
        base_parse = urlparse(base_url)
        un = UrlNormalizer
        sheme = un._parse_sheme(parse, base_parse)
        netloc = un._parse_netloc(parse, base_parse)
        path = un._parse_path(parse, base_parse)
        query = un._parse_query(parse)
        fragment = un._parse_fragment(parse)
        return sheme + netloc + path + query + fragment

    @staticmethod
    def image_name_helper(temp_path: str, name: str, idx) -> str:
        name = remove_file_query_params(name, False)
        basename = '{:0>3}_{}'.format(idx, name)
        name_loss = name.find('?') == 0
        name_len_loss = len(name) < 4
        name_dot_loss = name.find('.') < 1
        if name_loss or name_len_loss or name_dot_loss:
            basename = '{:0>3}.png'.format(idx)
        return path_join(temp_path, basename)

