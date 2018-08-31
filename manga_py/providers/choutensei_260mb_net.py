from .adulto_seinagi_org import AdultoSeinagiOrg


class ChouTensei260mbNet(AdultoSeinagiOrg):
    def prepare_cookies(self):
        self._storage['cookies'][' __test'] = '9f148766d926b07a85683d7a6cd50150'
        super().prepare_cookies()


main = ChouTensei260mbNet
