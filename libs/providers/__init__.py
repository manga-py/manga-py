import re

providers_list = {
    # # 'comic_walker_com': 'comic\\-walker\\.com/contents/detail/.+',
    'comicextra_com': 'comicextra\\.com/.+',
    'comico_jp': 'comico\\.jp/(detail|articleList).+titleNo.+',
    'comicsandmanga_ru': 'comicsandmanga\\.ru/online\\-reading/.+',
    'desu_me': 'desu\\.me/manga/.+',
    # 'eatmanga_me': 'eatmanga\\.me/.+',
    'funmanga_com': 'funmanga\\.com/.+',
    # 'gogomanga_co': 'gogomanga\\.co/.+',
    'goodmanga_net': 'goodmanga\\.net/.+',
    # 'heymanga_me': 'heymanga\\.me/manga/.+',
    'inmanga_com': 'inmanga\\.com/ver/manga/.+',
    'jurnalu_ru': 'jurnalu\\.ru/online\\-reading/.+',
    # 'kissmanga_com': 'kissmanga\\.com/Manga/.+',
    # 'manga_online_biz': 'manga\\-online\\.biz/.+',
    # 'manga_online_com_ua': 'manga\\-online\\.com\\.ua/.+',
    # 'mangabb_co': 'mangabb\\.co/.+',
    # 'mangabox_me': 'mangabox\\.me/reader/.+',
    # 'mangachan_me': 'mangachan\\.me/[^/]+/.+',
    # 'mangaclub_ru': 'mangaclub\\.ru/.+',
    # 'mangadoom_co': 'mangadoom\\.co/.+',
    # 'mangaeden_com': 'mangaeden\\.com/[^/]+/[^/]+\\-manga/.+',
    # 'mangafox_me': 'mangafox\\.me/manga/.+',
    # 'mangafreak_net': 'mangafreak\\.net/.+',  # with cf-protect
    # 'mangago_me': 'mangago\\.me/read\\-manga/.+',  # with cf-protect
    # 'mangahead_me': 'mangahead\\.me/.*Manga-\w+-Scan/.+',
    # 'mangahere_co': 'mangahere\\.co/manga/.+',
    # 'mangahome_com': 'mangahome\\.com/manga/.+',
    # 'mangahub_ru': 'mangahub\\.ru/.+',
    # 'mangainn_net': 'mangainn\\.net/manga/.+',
    # 'mangakakalot_com': 'mangakakalot\\.com/(manga|chapter)/.+',
    # 'mangaleader_com': 'mangaleader\\.com/read\\-.+',
    # 'mangalife_us': 'mangalife\\.us/(read-online|manga)/.+',
    # 'mangalib_me': 'mangalib\\.me/.+',
    # 'mangamove_com': 'mangamove\\.com/manga/.+',
    # 'manganel_com': 'manganel\\.com/(manga|chapter)/.+',
    # 'mangaonlinehere_com': 'mangaonlinehere\\.com/manga\\-info/.+',
    # 'mangaonline_today': 'mangaonline\\.today/.+',
    # 'mangapanda_com': 'mangapanda\\.com/.+',
    # 'mangapark_me': 'mangapark\\.me/manga/.+',
    # 'mangareader_net': 'mangareader\\.net/.+',
    # 'mangaroot_com': 'mangaroot\\.com/manga/.+',
    # 'mangarussia_com': 'mangarussia\\.com/manga/.+',
    # 'mangasaurus_com': 'mangasaurus\\.com/manga.+',
    # 'mangasupa_com': 'mangasupa\\.com/(manga|chapter).+',
    # 'mangatan_net': '(mangashin\\.com|mangatan\\.net)/(manga|chapter)',  # site renamed to mangashin.com
    # 'mangatown_com': 'mangatown\\.com/manga.+',
    # # 'mangaz_com': '\\.mangaz\\.com/.+',
    # 'manhuagui_com': 'manhuagui\\.com/comic/\\d+',
    # 'mintmanga_com': 'mintmanga\\.com/.+',
    # 'myreadingmanga_info': 'myreadingmanga\\.info/.+',  # with cf-protect
    # 'ninemanga_com': 'ninemanga\\.com/manga.+',
    # # 'onemanga_com': 'onemanga\\.com/manga.+',
    # 'read_yagami_me': 'read\\.yagami\\.me/.+',
    # 'readcomicbooksonline_net': 'readcomicbooksonline\\.net/.+',
    # 'readcomiconline_to': 'readcomiconline\\.to/Comic/.+',
    'readmanga_me': 'readmanga\\.me/.+',
    # 'readmanga_eu': 'readmanga\\.eu/manga/\d+/.+',
    # 'readms_net': 'readms\\.net/(r|manga)/.+',
    # 'selfmanga_ru': 'selfmanga\\.ru/.+',
    # 'shakai_ru': 'shakai\\.ru/manga.*?/\d+',
    # 'somanga_net': 'somanga\\.net/.+',
    # 'taadd_com': 'taadd\\.com/(book|chapter)/.+',
    # 'tapas_io': 'tapas\\.io/(series|episode)/.+',
    # 'tenmanga_com': 'tenmanga\\.com/(book|chapter)/.+',
    # 'unixmanga_nl': 'unixmanga\\.nl/onlinereading/.+\\.html',
    # 'wmanga_ru': 'wmanga\\.ru/starter/manga_.+',
    # 'viz_com': 'viz\\.com/shonenjump/chapters/.+',
    # 'yaoichan_me': 'yaoichan\\.me/(manga|online).+',
    # 'zingbox_me': 'zingbox\\.me/.+',
    # 'zip_read_com': 'zip\\-read\\.com/.+',
    #
    # 'otakusmash_com': '(otakusmash\\.com|mrsmanga\\.com|mentalmanga\\.com)'
}


def get_provider(url):
    for i in providers_list:
        result = re.search(providers_list[i], url)
        if result is not None:
            provider = __import__('libs.providers.{}'.format(i), fromlist=['libs.providers'])
            return provider.main
    return False
