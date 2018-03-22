from manga_dl.providers.gomanga_co import GoMangaCo


class MangaJinnoFansubCom(GoMangaCo):
    _name_re = '/lector/[^/]+/([^/]+)'
    _content_str = '{}/lector/{}'

main = MangaJinnoFansubCom
