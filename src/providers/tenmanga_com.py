from src.providers.taadd_com import TaaddCom


class TenMangaCom(TaaddCom):
    _name_selector = '.read-page a[href*="/book/"]'
    _pages_selector = '.sl-page'
    _chapters_selector = '.chapter-box .choose-page a:last-child'

    @staticmethod
    def _get_image(parser):
        items = parser.cssselect('.pic_box .manga-pic')
        return [i.get('src') for i in items]


main = TenMangaCom
