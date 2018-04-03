from .gomanga_co import GoMangaCo


class LoliVaultNet(GoMangaCo):
    _name_re = '/online/[^/]+/([^/]+)/'
    _content_str = '{}/online/series/{}/'
    _chapters_selector = '.list .group .element .title a'


main = LoliVaultNet
