from .taadd_com import TaaddCom
from time import sleep


class TenMangaCom(TaaddCom):
    __manga_url = 'https://www.gardenmanage.com/c/tenmanga/'
    _name_selector = '.read-page a[href*="/book/"]'
    _pages_selector = '.sl-page'
    _chapters_selector = '.chapter-name.long > a'
    img_selector = '.pic_box .manga_pic'

    def get_files(self):
        try:
            content = self.http_get(self.chapter)
        except ConnectionError:
            sleep(.2)
            content = self.http_get(self.chapter)

        images = self.re.search(r'all_imgs_url.+?\[((?:\s*"http.+?",?)+)', content)

        if not images:
            return []

        images = self.re.sub(r'["\s*]', '', images.group(1))
        images = images.rstrip(',').split(',')
        return images


main = TenMangaCom
