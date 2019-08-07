from .hentaifox_com import HentaiFoxCom


class HentaiHandCom(HentaiFoxCom):
    _idx_re = r'/comic/(\d+)'
    _url_str = '{}/comic/{}/'
    _name_selector = '#info h1'
    _archive_prefix = 'HentaiHand_'

    def get_files(self):
        parser = self.document_fromstring(self.content)
        images = self._images_helper(parser, 'a.gallerythumb > img')
        re = self.re.compile(r'(.+/images/)(\d+)')
        return ['{}full/{}.jpg'.format(*re.search(i).groups()) for i in images]


main = HentaiHandCom
