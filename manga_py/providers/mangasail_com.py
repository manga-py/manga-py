from .mangatail_com import MangaTailCom


class MangaSailCom(MangaTailCom):
    def get_chapters(self):
        return super().get_chapters()[::-1]


main = MangaSailCom
