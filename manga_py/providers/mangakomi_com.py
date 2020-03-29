from .mangazuki_me import MangaZukiMe


class MangaKomiCom(MangaZukiMe):

    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(
            parser, 'img.wp-manga-chapter-img',
            attr='data-lazy-src', alternative_attr='src'
        )


main = MangaKomiCom
