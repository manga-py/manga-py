from src.providers.mangalife_us import MangaLifeUs


class MangaSeeOnlineUs(MangaLifeUs):

    def _get_image(self, parser):
        return parser.cssselect('.image-container-manga .CurImage')[0].get('src')


main = MangaSeeOnlineUs
