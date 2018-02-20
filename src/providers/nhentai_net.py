from src.providers.hentaifox_com import HentaiFoxCom


class nHentaiNet(HentaiFoxCom):
    _idx_re = r'/g/(\d+)'
    _url_str = '{}/g/{}/'
    _name_re = '#info h1'
    _cdn = 'https://i.nhentai.net/galleries/'
    __ext = {'j': 'jpg', 'p': 'png', 'g': 'gif'}

    def get_files(self):
        c, s = self.get_storage_content(), '#thumbnail-container a'
        page = self.document_fromstring(c, s, 0)
        n = self.http().normalize_uri
        content = self.http_get(n(page.get('href')))
        imgs = self.re.search(r'gallery\s*:\s*(\{.+\}),', content)
        imgs = self.json.loads(imgs.group(1))
        idx = imgs.get('media_id')
        images = []
        for n, i in enumerate(imgs.get('images', {}).get('pages', [])):
            images.append('{}{}/{}.{}'.format(self._cdn, idx, n+1, self.__ext.get(i.get('t'))))
        print(images)
        exit()
        return images

    def get_cover(self) -> str:
        return self._cover_from_content('#cover img', 'data-src')

    def prepare_cookies(self):
        p = '208.95.62.80:3128'
        self._storage['proxies'] = {'http': p, 'https': p}
        print(self._storage['proxies'])


main = nHentaiNet
