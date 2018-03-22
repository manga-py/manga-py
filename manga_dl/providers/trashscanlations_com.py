from .zeroscans_com import ZeroScansCom


class TrashScanlationsCom(ZeroScansCom):
    def get_main_content(self):
        return self._get_content('{}/series/{}/')

    def get_manga_name(self) -> str:
        return self._get_name('/series/([^/]+)')


main = TrashScanlationsCom
