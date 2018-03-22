from manga_dl.providers.mangalife_us import MangaLifeUs


class MangaSeeOnlineUs(MangaLifeUs):
    img_selector = '.image-container-manga .CurImage'


main = MangaSeeOnlineUs
