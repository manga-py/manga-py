from src.providers.read_powermanga_org import ReadPowerMangaOrg


class Pzykosis666HFansubCom(ReadPowerMangaOrg):
    _name_re = '/online/[^/]+/([^/]+)/'
    _content_str = '{}/online/series/{}/'

    def prepare_cookies(self):
        data = {'adult': 'true'}
        url = self.get_url()
        response = self.http()._requests(method='post', data=data, url=url)
        cookies = response.cookies.items()
        for i in cookies:
            self._storage['cookies'][i[0]] = i[1]


main = Pzykosis666HFansubCom
