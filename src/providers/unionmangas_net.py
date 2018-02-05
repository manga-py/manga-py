from src.providers.somanga_net import SoMangaNet


class UnionMangasNet(SoMangaNet):

    def get_chapters(self):
        selector = '.tamanho-bloco-perfil .lancamento-linha a[href*="/leitor/"]'
        parser = self.document_fromstring(self.get_storage_content(), selector)
        return [i.get('href') for i in parser]


main = UnionMangasNet
