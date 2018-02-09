from src.providers.hentaifox_com import HentaiFoxCom

from urllib.parse import urlparse


class HitomiLa(HentaiFoxCom):
    _idx_re = r'/(?:galleries|reader)/(\d+)'
    _url_str = '{}/gallery/{}/'
    _name_re = '.manga-gallery h1 a'

    def get_manga_name(self):
        name = super().get_manga_name()
        return name.split('|')[0].strip()

    def get_files(self):
        content = self.get_storage_content()
        src = self.html_fromstring(content, 'script[src*="hitomi.la"]', 0).get('src')
        scheme = urlparse(self.get_url()).scheme
        domain = urlparse(src).netloc
        idx = self.re.search(self._idx_re, self._url_str).group(1)
        url = '{}://{}/galleries/{}.js'.format(scheme, domain, idx)
        images = self.re.search(r'(\[.+\])', self.http_get(url))
        images = self.json.loads(images)
        return ['{}://{}/galleries/{}/{}'.format(scheme, domain, idx, i.get('name')) for i in images]


main = HitomiLa
