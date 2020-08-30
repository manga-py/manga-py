from .rawdevart_com_old import RawDevArtComOld


class ThreeAsqOrg(RawDevArtComOld):

    def get_chapter_index(self) -> str:
        return self.chapter.split('/')[-2]
    
    def get_files(self):
        parser = self.html_fromstring(self.chapter)
        return self._images_helper(parser, 'img.wp-manga-chapter-img')

    @property
    def chapter(self):
        return super().chapter + '?style=list'


main = ThreeAsqOrg
