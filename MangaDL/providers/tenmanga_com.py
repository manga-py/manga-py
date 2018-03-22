from .taadd_com import TaaddCom


class TenMangaCom(TaaddCom):
    _name_selector = '.read-page a[href*="/book/"]'
    _pages_selector = '.sl-page'
    _chapters_selector = '.chapter-box .choose-page a:last-child'
    img_selector = '.pic_box .manga_pic'


main = TenMangaCom
