from src.providers.readmanga_me import ReadmangaMe


class SelfMangaRu(ReadmangaMe):

    def get_manga_name(self):
        return self.re.search('\\.ru/([^/]+)', self.get_url()).group(1)

main = SelfMangaRu
