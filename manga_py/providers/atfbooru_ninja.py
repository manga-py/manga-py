from .danbooru_donmai_us import DanbooruDonmaiUs


class AtfBooruNinja(DanbooruDonmaiUs):
    _archive_prefix = 'atfbooru'


main = AtfBooruNinja
