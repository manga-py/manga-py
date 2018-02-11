import re


providers_list = {
    'adulto_seinagi_org': [r'adulto\.seinagi\.org/(series|read)/.'],
    'blogtruyen_com': [r'blogtruyen\.com/.'],
    'comicextra_com': [r'comicextra\.com/.'],
    'comico_jp': [r'comico\.jp/(detail|articleList).+titleNo.'],
    'comicsandmanga_ru': [r'comicsandmanga\.ru/online\-reading/.'],
    'dejameprobar_es': [
        r'dejameprobar\.es/slide/.',
        r'menudo\-fansub\.com/slide/.',
        r'npscan\.mangaea\.net/slide/.',
        r'snf\.mangaea\.net/slide/.',
    ],
    'desu_me': [r'desu\.me/manga/.'],
    'doujins_com': [r'doujins\.com/gallery/.'],
    'e_hentai_org': [r'e\-hentai\.org/g/\d'],
    'funmanga_com': [r'funmanga\.com/.'],
    'gmanga_me': [r'gmanga\.me/mangas/.'],
    'gomanga_co': [r'gomanga\.co/reader/.'],
    'goodmanga_net': [r'goodmanga\.net/.'],
    'hakihome_com': [r'hakihome\.com/.'],
    'hentai2read_com': [r'hentai2read\.com/.'],
    'hentai_cafe': [r'hentai\.cafe/.'],
    'hentai_chan_me': [r'hentai\-chan\.me/(related|manga|online)/.'],
    'hentai_chan_me_download': [r'hentai\-chan\.me/download/.'],
    'hentaifox_com': [r'hentaifox\.com/.'],
    'hitomi_la': [r'hitomi\.la/(galleries|reader)/.'],
    'hocvientruyentranh_com': [r'http://hocvientruyentranh\.com/(manga|chapter)/.'],
    'inmanga_com': [r'inmanga\.com/ver/manga/.'],
    'jaiminisbox_com': [
        r'jaiminisbox\.com/reader/.',
        r'kobato\.hologfx\.com/reader/.',
        r'atelierdunoir\.org/reader/.'
        r'seinagi\.org/reader/.'
    ],
    'japscan_com': [r'japscan\.com/.'],
    'jurnalu_ru': [r'jurnalu\.ru/online\-reading/.'],
    'kissmanga_com': [r'kissmanga\.com/Manga/.'],
    'kumanga_com': [r'kumanga\.com/manga/\d'],
    'leomanga_com': [r'leomanga\.com/manga/.'],
    'manga_online_biz': [r'manga\-online\.biz/.'],
    'manga_online_com_ua': [r'manga\-online\.com\.ua/.+html'],
    'mangabb_co': [r'mangabb\.co/.'],
    'mangabox_me': [r'mangabox\.me/reader/.'],
    'mangachan_me': [r'mangachan\.me/(related|manga|online)/.'],
    'mangachan_me_download': [r'mangachan\.me/download/.'],
    'mangaclub_ru': [r'mangaclub\.ru/.'],
    'mangaeden_com': [r'mangaeden\.com/[^/]+/[^/]+\-manga/.'],
    # 'mangafox_la': [r'mangafox\.(me|la)/manga/.'],
    'mngdoom_com': [r'(mangadoom\.co|mngdoom\.com)/.'],
    'mangago_me': [r'mangago\.me/read\-manga/.'],
    'mangahere_co': [r'mangahere\.(co|cc)/manga/.'],
    'mangahome_com': [r'mangahome\.com/manga/.'],
    'mangahub_ru': [r'mangahub\.ru/.'],
    'mangainn_net': [r'mangainn\.net/.'],
    'mangakakalot_com': [r'mangakakalot\.com/(manga|chapter)/.'],
    'mangalib_me': [r'mangalib\.me/.'],
    'mangalife_us': [r'mangalife\.us/(read\-online|manga)/.'],
    'mangaonline_today': [r'mangaonline\.today/.'],
    'mangaonlinehere_com': [r'mangaonlinehere\.com/(manga\-info|read\-online)/.'],
    'mangapanda_com': [r'mangapanda\.com/.'],
    'mangapark_me': [r'mangapark\.me/manga/.'],
    'mangareader_net': [r'mangareader\.net/.'],
    'mangarussia_com': [r'mangarussia\.com/(manga|chapter)/.'],
    'mangasaurus_com': [r'mangasaurus\.com/manga.'],
    'mangasupa_com': [r'mangasupa\.com/(manga|chapter).'],
    'mangatown_com': [r'mangatown\.com/manga.'],
    'manhuagui_com': [r'manhuagui\.com/comic/\d'],
    'mintmanga_com': [r'mintmanga\.com/.'],
    'myreadingmanga_info': [r'myreadingmanga\.info/.'],
    'ninemanga_com': [r'ninemanga\.com/(manga|chapter).'],
    'otakusmash_com': [
        r'otakusmash\.com/.',
        r'mrsmanga\.com/.',
        r'mentalmanga\.com/.',
        r'mangasmash\.com/.'
    ],
    'otscans_com': [r'otscans\.com/foolslide/(series|read)/.'],
    'pzykosis666hfansub_com': [r'pzykosis666hfansub\.com/online/.'],
    'read_powermanga_org': [
        r'lector\.dangolinenofansub\.com/(read|series)/.',
        r'read\.powermanga\.org/(read|series)/.',
        r'read\.yagami\.me/(series|read)/.',
        r'reader\.championscans\.com/(series|read)/.',
        r'reader\.kireicake\.com/(series|read)/.',
        r'reader\.shoujosense\.com/(series|read)/.',
        r'reader\.sensescans\.com/(series|read)/.',
        r'reader\.whiteoutscans\.com/(series|read)/.'
        r'slide\.world\-three\.org/(series|read)/.'
        r'manga\.animefrontline\.com/(series|read)/.'
    ],
    'readcomicbooksonline_org': [
        r'readcomicbooksonline\.net/.',
        r'readcomicbooksonline\.org/.'
    ],
    'readcomiconline_to': [r'readcomiconline\.to/Comic/.'],
    'readmanga_me': [r'readmanga\.me/.'],
    'readmanga_eu': [r'readmanga\.eu/manga/\d+/.'],
    'readms_net': [r'readms\.net/(r|manga)/.'],
    'santosfansub_com': [r'santosfansub\.com/Slide/.'],
    'selfmanga_ru': [r'selfmanga\.ru/.'],
    'shakai_ru': [r'shakai\.ru/manga.*?/\d'],
    'somanga_net': [r'somanga\.net/(leitor|manga)/.'],
    'taadd_com': [r'taadd\.com/(book|chapter)/.'],
    'tenmanga_com': [r'tenmanga\.com/(book|chapter)/.'],
    'unionmangas_net': [r'unionmangas\.net/(leitor|manga)/.'],
    # 'viz_com': [r'viz\.com/shonenjump/chapters/.'],
    'wmanga_ru': [r'wmanga\.ru/starter/manga_.'],
    'yaoichan_me': [r'yaoichan\.me/(manga|online).'],
    'yaoichan_me_download': [r'yaoichan\.me/download/.'],
    'zingbox_me': [r'zingbox\.me/.'],
    'zip_read_com': [r'zip\-read\.com/.']
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
