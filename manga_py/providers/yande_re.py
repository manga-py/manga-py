from .lolibooru_moe import LoliBooruMoe


class YandeRe(LoliBooruMoe):
    _archive_prefix = 'yandere_'


main = YandeRe
