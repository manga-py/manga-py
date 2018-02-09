from .readmanga_me import ReadmangaMe


class MintMangaCom(ReadmangaMe):

    def get_manga_name(self):
        return self.re.search(r'\.com/([^/]+)', self.get_url()).group(1)


main = MintMangaCom
