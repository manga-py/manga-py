from .gomanga_co import GoMangaCo

from .helpers.std import Std


class HentaiCafe(GoMangaCo, Std):
    _name_re = r'\.cafe(?:/manga/read)?/([^/]+)/'
    _content_str = '{}/{}/'
    _chapters_selector = '.content .last .x-btn'  # TODO

    def get_archive_name(self) -> str:
        return 'archive_{:0>2}'.format(self.chapter_id)

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def get_cover(self) -> str:
        return self._cover_from_content('.entry-content img')


main = HentaiCafe
