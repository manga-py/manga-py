from .somanga_net import SoMangaNet


class UnionMangasNet(SoMangaNet):

    def get_chapters(self):
        selector = '.tamanho-bloco-perfil .lancamento-linha a[href*="/leitor/"]'
        return self.document_fromstring(self.content, selector)


main = UnionMangasNet
