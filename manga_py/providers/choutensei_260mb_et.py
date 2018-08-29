from .adulto_seinagi_org import AdultoSeinagiOrg


class ChouTensei260mbNet(AdultoSeinagiOrg):
    def get_main_content(self):
        content = super().get_main_content()
        # TODO: need solve!
        return content


main = ChouTensei260mbNet
