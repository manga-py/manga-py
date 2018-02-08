import re


providers_list = {
    'adulto_seinagi_org': ['adulto\\.seinagi\\.org/(series|read)/.'],
    'blogtruyen_com': ['blogtruyen\\.com/.'],
    'comicextra_com': ['comicextra\\.com/.'],
    'comico_jp': ['comico\\.jp/(detail|articleList).+titleNo.'],
    'comicsandmanga_ru': ['comicsandmanga\\.ru/online\\-reading/.'],
    'dejameprobar_es': [
        'dejameprobar\\.es/slide/.',
        'menudo\\-fansub\\.com/slide/.',
        'npscan\\.mangaea\\.net/slide/.',
        'snf\\.mangaea\\.net/slide/.',
    ],
    'desu_me': ['desu\\.me/manga/.'],
    'doujins_com': ['doujins\\.com/gallery/.'],
    'e_hentai_org': ['e\\-hentai\\.org/g/\\d'],
    'funmanga_com': ['funmanga\\.com/.'],
    'gmanga_me': ['gmanga\\.me/mangas/.'],
    'gomanga_co': ['gomanga\\.co/reader/.'],
    'goodmanga_net': ['goodmanga\\.net/.'],
    'hentai_chan_me': ['hentai\\-chan\\.me/(related|manga|online)/.'],
    'hentai_chan_me_download': ['hentai\\-chan\\.me/download/.'],
    'hocvientruyentranh_com': ['http://hocvientruyentranh\\.com/(manga|chapter)/.'],
    'inmanga_com': ['inmanga\\.com/ver/manga/.'],
    'jaiminisbox_com': [
        'jaiminisbox\\.com/reader/.',
        'kobato\\.hologfx\\.com/reader/.',
        'atelierdunoir\\.org/reader/.'
        'seinagi\\.org/reader/.'
    ],
    'jurnalu_ru': ['jurnalu\\.ru/online\\-reading/.'],
    'kissmanga_com': ['kissmanga\\.com/Manga/.'],
    'manga_online_biz': ['manga\\-online\\.biz/.'],
    'manga_online_com_ua': ['manga\\-online\\.com\\.ua/.+html'],
    'mangabb_co': ['mangabb\\.co/.'],
    'mangabox_me': ['mangabox\\.me/reader/.'],
    'mangachan_me': ['mangachan\\.me/(related|manga|online)/.'],
    'mangachan_me_download': ['mangachan\\.me/download/.'],
    'mangaclub_ru': ['mangaclub\\.ru/.'],
    'mangaeden_com': ['mangaeden\\.com/[^/]+/[^/]+\\-manga/.'],
    # 'mangafox_la': ['mangafox\\.(me|la)/manga/.'],
    'mngdoom_com': ['(mangadoom\\.co|mngdoom\\.com)/.'],
    'mangago_me': ['mangago\\.me/read\\-manga/.'],
    'mangahere_co': ['mangahere\\.(co|cc)/manga/.'],
    'mangahome_com': ['mangahome\\.com/manga/.'],
    'mangahub_ru': ['mangahub\\.ru/.'],
    'mangainn_net': ['mangainn\\.net/.'],
    'mangakakalot_com': ['mangakakalot\\.com/(manga|chapter)/.'],
    'mangalib_me': ['mangalib\\.me/.'],
    'mangalife_us': ['mangalife\\.us/(read\\-online|manga)/.'],
    'mangaonline_today': ['mangaonline\\.today/.'],
    'mangaonlinehere_com': ['mangaonlinehere\\.com/(manga\\-info|read\\-online)/.'],
    'mangapanda_com': ['mangapanda\\.com/.'],
    'mangapark_me': ['mangapark\\.me/manga/.'],
    'mangareader_net': ['mangareader\\.net/.'],
    'mangarussia_com': ['mangarussia\\.com/(manga|chapter)/.'],
    'mangasaurus_com': ['mangasaurus\\.com/manga.'],
    'mangasupa_com': ['mangasupa\\.com/(manga|chapter).'],
    'mangatown_com': ['mangatown\\.com/manga.'],
    'manhuagui_com': ['manhuagui\\.com/comic/\\d'],
    'mintmanga_com': ['mintmanga\\.com/.'],
    'myreadingmanga_info': ['myreadingmanga\\.info/.'],
    'ninemanga_com': ['ninemanga\\.com/(manga|chapter).'],
    'otakusmash_com': [
        'otakusmash\\.com/.',
        'mrsmanga\\.com/.',
        'mentalmanga\\.com/.',
        'mangasmash\\.com/.'
    ],
    'otscans_com': ['otscans\\.com/foolslide/(series|read)/.'],
    'pzykosis666hfansub_com': ['pzykosis666hfansub\\.com/online/.'],
    'read_powermanga_org': [
        'lector\\.dangolinenofansub\\.com/(read|series)/.',
        'read\\.powermanga\\.org/(read|series)/.',
        'read\\.yagami\\.me/(series|read)/.',
        'reader\\.championscans\\.com/(series|read)/.',
        'reader\\.kireicake\\.com/(series|read)/.',
        'reader\\.shoujosense\\.com/(series|read)/.',
        'reader\\.sensescans\\.com/(series|read)/.',
        'reader\\.whiteoutscans\\.com/(series|read)/.'
        'slide\\.world\\-three\\.org/(series|read)/.'
        'manga\\.animefrontline\\.com/(series|read)/.'
    ],
    'readcomicbooksonline_org': [
        'readcomicbooksonline\\.net/.',
        'readcomicbooksonline\\.org/.'
    ],
    'readcomiconline_to': ['readcomiconline\\.to/Comic/.'],
    'readmanga_me': ['readmanga\\.me/.'],
    'readmanga_eu': ['readmanga\\.eu/manga/\d+/.'],
    'readms_net': ['readms\\.net/(r|manga)/.'],
    'santosfansub_com': ['santosfansub\\.com/Slide/.'],
    'selfmanga_ru': ['selfmanga\\.ru/.'],
    'shakai_ru': ['shakai\\.ru/manga.*?/\\d'],
    'somanga_net': ['somanga\\.net/(leitor|manga)/.'],
    'taadd_com': ['taadd\\.com/(book|chapter)/.'],
    'tenmanga_com': ['tenmanga\\.com/(book|chapter)/.'],
    'unionmangas_net': ['unionmangas\\.net/(leitor|manga)/.'],
    # 'viz_com': ['viz\\.com/shonenjump/chapters/.'],
    'wmanga_ru': ['wmanga\\.ru/starter/manga_.'],
    'yaoichan_me': ['yaoichan\\.me/(manga|online).'],
    'yaoichan_me_download': ['yaoichan\\.me/download/.'],
    'zingbox_me': ['zingbox\\.me/.'],
    'zip_read_com': ['zip\\-read\\.com/.']
}


def __check_provider(provider, url):
    reg = '(?:' + '|'.join(provider) + ')'
    return re.search(reg, url)


def get_provider(url):
    for i in providers_list:
        if __check_provider(providers_list[i], url):
            provider = __import__('src.providers.{}'.format(i), fromlist=['src.providers'])
            return provider.main
    return False
