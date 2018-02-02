from .readmanga_me import ReadmangaMe


class MintMangaCom(ReadmangaMe):

    def get_manga_name(self):
        return self.re_search('\\.com/([^/]+)', self.get_url()).group(1)


main = MintMangaCom
