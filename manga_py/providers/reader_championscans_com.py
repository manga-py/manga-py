from .read_powermanga_org import ReadPowerMangaOrg


class ReaderChampionScansCom(ReadPowerMangaOrg):

    def get_chapter_index(self):
        idx = super().get_chapter_index().split('-')
        if idx[0] == '0':
            del idx[0]
        return '-'.join(idx)


main = ReaderChampionScansCom
