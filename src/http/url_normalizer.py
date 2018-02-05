from urllib.parse import urlparse

from src.fs import remove_file_query_params, path_join


class UrlNormalizer:

    @staticmethod
    def __relative_scheme(uri, ref):
        scheme = urlparse(ref).scheme if ref else 'http'
        return scheme + ':' + uri

    @staticmethod
    def __get_domain(uri, ref):
        new_url = ref[:ref.rfind('/')]
        if uri.find('/') == 0:
            new_url = urlparse(ref)
            new_url = '{}://{}'.format(new_url.scheme, new_url.netloc)
        return new_url

    @staticmethod
    def url_helper(url: str, base_url: str) -> str:
        if url.find('//') == 0:  # abs without scheme
            return UrlNormalizer.__relative_scheme(url, base_url)
        if url.find('://') < 1:  # relative
            _ = UrlNormalizer.__get_domain(url, base_url)
            return '{}/{}'.format(_.rstrip('/'), url.lstrip('/'))
        return url

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

