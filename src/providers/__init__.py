import re

providers_list = {
    'adulto_seinagi_org': [
        r'adulto\.seinagi\.org/(series|read)/.',
        r'xanime-seduccion\.com/(series|read)/.',
    ],
    'animextremist_com': [
        r'animextremist\.com/mangas-online/.',
    ],
    'antisensescans_com': [
        r'antisensescans\.com/online/(series|read)/.',
    ],
    'authrone_com': [
        r'authrone\.com/manga/.',
    ],
    'bato_to': [
        r'bato\.to/(series|chapter)/\d',
    ],
    'blogtruyen_com': [
        r'blogtruyen\.com/.',
    ],
    'chochox_com': [
        r'chochox\.com/.',
    ],
    'comicextra_com': [
        r'comicextra\.com/.',
    ],
    'comic_webnewtype_com': [
        r'comic\.webnewtype\.com/contents/.',
    ],
    'comico_jp': [
        r'comico\.jp/(detail|articleList).+titleNo.',
    ],
    'comicsandmanga_ru': [
        r'comicsandmanga\.ru/online-reading/.',
    ],
    'darkskyprojects_org': [
        r'darkskyprojects\.org/biblioteca/.',
    ],
    'dejameprobar_es': [
        r'dejameprobar\.es/slide/.',
        r'menudo-fansub\.com/slide/.',
        r'npscan\.mangaea\.net/slide/.',
        r'snf\.mangaea\.net/slide/.',
    ],
    'desu_me': [
        r'desu\.me/manga/.',
    ],
    'doujins_com': [
        r'doujins\.com/gallery/.',
        r'doujin-moe\.us/gallery/.',
    ],
    'e_hentai_org': [
        r'e-hentai\.org/g/\d',
    ],
    'eight_muses_com': [
        r'8muses\.com/comics/album/.',
    ],
    'freeadultcomix_com': [
        r'freeadultcomix\.com/.',
    ],
    'funmanga_com': [
        r'funmanga\.com/.',
    ],
    'gmanga_me': [
        r'gmanga\.me/mangas/.',
    ],
    'gomanga_co': [
        r'gomanga\.co/reader/.',
        r'jaiminisbox\.com/reader/.',
        r'kobato\.hologfx\.com/reader/.',
        r'atelierdunoir\.org/reader/.',
        r'seinagi\.org/reader/.',
    ],
    'goodmanga_net': [
        r'goodmanga\.net/.',
    ],
    'helveticascans_com': [
        r'helveticascans\.com/r/(series|read)/.',
    ],
    'hakihome_com': [
        r'hakihome\.com/.',
    ],
    'heavenmanga_biz': [
        r'heavenmanga\.biz/.',
    ],
    'hentai2read_com': [
        r'hentai2read\.com/.',
    ],
    'hentai_cafe': [
        r'hentai\.cafe/.',
    ],
    'hentai_chan_me': [
        r'hentai-chan\.me/(related|manga|online)/.',  # todo
    ],
    'hentaifox_com': [
        r'hentaifox\.com/.',
    ],
    'hentaihere_com': [
        r'hentaihere\.com/m/.',
    ],
    'hentairead_com': [
        r'hentairead\.com/.',
    ],
    'hitomi_la': [
        r'hitomi\.la/(galleries|reader)/.',
    ],
    'hitmanga_eu': [
        r'hitmanga\.eu/.',
        r'mymanga\.io/.',
    ],
    'hocvientruyentranh_com': [
        r'hocvientruyentranh\.com/(manga|chapter)/.',
    ],
    'hotchocolatescans_com': [
        r'hotchocolatescans\.com/fs/(series|read)/.',
        r'mangaichiscans\.mokkori\.fr/fs/(series|read)/.',
    ],
    'inmanga_com': [
        r'inmanga\.com/ver/manga/.',
    ],
    'japscan_com': [
        r'japscan\.com/.',
    ],
    'jurnalu_ru': [
        r'jurnalu\.ru/online-reading/.',
    ],
    'kissmanga_com': [
        r'kissmanga\.com/Manga/.',
    ],
    'kumanga_com': [
        r'kumanga\.com/manga/\d',
    ],
    'lector_kirishimafansub_com': [
        r'lector\.kirishimafansub\.com/(lector/)?(series|read)/.',
    ],
    'leomanga_com': [
        r'leomanga\.com/manga/.',
    ],
    'luscious_net': [
        r'luscious\.net/c/incest_manga/pictures/.', r'luscious\.net/albums/.',
    ],
    'manga_ae': [
        r'manga\.ae/.',
    ],
    'manga_online_biz': [
        r'manga-online\.biz/.',
    ],
    'manga_online_com_ua': [
        r'manga-online\.com\.ua/.+html',
    ],
    'manga_sh': [
        r'manga\.sh/comics/.',
    ],
    'manga_tube_me': [
        r'manga-tube\.me/series/.',
    ],
    'manga_tr_com': [
        r'manga-tr\.com/(manga|id)-.',
    ],
    'mangabb_co': [
        r'mangabb\.co/.',
    ],
    'mangabox_me': [
        r'mangabox\.me/reader/.',
    ],
    'mangachan_me': [
        r'mangachan\.me/(related|manga|online)/.',
        r'yaoichan\.me/(manga|online).',
    ],
    'mangachan_me_download': [
        r'mangachan\.me/download/.',
        r'hentai-chan.me/download/.',
        r'yaoichan\.me/download/.',
    ],
    'mangacanblog_com': [
        r'mangacanblog\.com/.',
    ],
    'mangaclub_ru': [
        r'mangaclub\.ru/.',
    ],
    'mangadeep_com': [
        r'mangadeep\.com/.',
    ],
    'mangadex_com': [
        r'mangadex\.com/(manga|chapter)/.',
    ],
    'mangaeden_com': [
        r'mangaeden\.com/[^/]+/[^/]+-manga/.',
        r'perveden\.com/[^/]+/[^/]+-manga/.',
    ],
    'mangaforall_com': [
        r'mangaforall\.com/m/.',
    ],
    'mangago_me': [
        r'mangago\.me/read-manga/.',
    ],
    'mangahere_cc': [
        r'mangahere\.co/manga/.',
        r'mangahere\.cc/manga/.',
    ],
    'mangahome_com': [
        r'mangahome\.com/manga/.',
    ],
    'mangahub_io': [
        r'mangahub\.io/(manga|chapter)/.',
        r'mangareader\.site/(manga|chapter)/.',
        r'mangakakalot\.fun/(manga|chapter)/.',
    ],
    'mangahub_ru': [
        r'mangahub\.ru/.',
    ],
    'mangaindo_web_id': [
        r'mangaindo\.web\.id/.',
    ],
    'mangainn_net': [
        r'mangainn\.net/.',
    ],
    'mangakakalot_com': [
        r'mangakakalot\.com/(manga|chapter)/.',
    ],
    'mangaku_web_id': [
        r'mangaku\.web\.id/.',
    ],
    'mangalib_me': [
        r'mangalib\.me/.',
    ],
    'mangalife_us': [
        r'mangalife\.us/(read-online|manga)/.',
    ],
    'mangaon_net': [
        r'mangaon\.net/(manga-info|read-online)/.',
    ],
    'mangaonline_com_br': [
        r'mangaonline\.com\.br/.',
    ],
    'mangaonline_today': [
        r'mangaonline\.today/.',
    ],
    'mangaonlinehere_com': [
        r'mangaonlinehere\.com/(manga-info|read-online)/.',
    ],
    'mangapanda_com': [
        r'mangapanda\.com/.',
    ],
    'mangapark_me': [
        r'mangapark\.me/manga/.',
    ],
    'mangareader_net': [
        r'mangareader\.net/.',
    ],
    'mangarock_com': [
        r'mangarock\.com/manga/.',
    ],
    'mangarussia_com': [
        r'mangarussia\.com/(manga|chapter)/.',
    ],
    'mangasaurus_com': [
        r'mangasaurus\.com/(manga|view).',
    ],
    'mangaseeonline_us': [
        r'mangaseeonline\.us/(read-online|manga)/.',
    ],
    'mangashiro_net': [
        r'mangashiro.net/.',
    ],
    'mangasupa_com': [
        r'mangasupa\.com/(manga|chapter)/.',
    ],
    'mangatail_com': [
        r'mangatail.com/(manga|chapter|node|content)/.',
        r'mangasail.com/(manga|chapter|node|content)/.',
    ],
    'mangatown_com': [
        r'mangatown\.com/manga/.',
    ],
    'manhuagui_com': [
        r'manhuagui\.com/comic/\d',
    ],
    'manhuatai_com': [
        r'manhuatai\.com/.',
    ],
    'manhwa_co': [
        r'manhwa\.co/.',
    ],
    'mangazuki_co': [
        r'mangazuki\.co/manga/.',
        r'mangaforest\.com/manga/.',
    ],
    'merakiscans_com': [
        r'merakiscans\.com/.',
    ],
    'mintmanga_com': [
        r'mintmanga\.com/.',
    ],
    'mngcow_co': [
        r'mngcow\.co/.',
    ],
    'mngdoom_com': [
        r'mangadoom\.co/.',
        r'mngdoom\.com/.',
    ],
    'myreadingmanga_info': [
        r'myreadingmanga\.info/.',
    ],
    'neumanga_tv': [
        r'neumanga\.tv/manga/.',
    ],
    'nhentai_net': [
        r'nhentai\.net/g/.',
    ],
    'nightow_net': [
        r'nightow\.net/online/\?manga=.',
    ],
    'ninemanga_com': [
        r'ninemanga\.com/(manga|chapter).',
    ],
    'noranofansub_com': [
        r'noranofansub\.com(/lector)?/(series/|read/)?.',
    ],
    'nozominofansub_com': [  # mangazuki_co
        r'nozominofansub\.com/public(/index.php)?/manga/.',
    ],
    'otakusmash_com': [
        r'otakusmash\.com/.',
        r'mrsmanga\.com/.',
        r'mentalmanga\.com/.',
        r'mangasmash\.com/.',
    ],
    'otscans_com': [
        r'otscans\.com/foolslide/(series|read)/.',
    ],
    'pecintakomik_com_manga': [
        r'pecintakomik\.com/manga/.',
    ],
    'pecintakomik_com': [
        r'pecintakomik\.com/.',
    ],
    'porncomix_info': [
        r'porncomix\.info/.',
    ],
    'psychoplay_co': [
        r'psychoplay\.co/(series|read)/.',
    ],
    'puzzmos_com': [
        r'puzzmos\.com/manga/.',
    ],
    r'pururin_io': [
        r'pururin\.io/(gallery|read)/.',
    ],
    'pzykosis666hfansub_com': [
        r'pzykosis666hfansub\.com/online/.',
    ],
    'read_powermanga_org': [
        r'lector\.dangolinenofansub\.com/(read|series)/.',
        r'read\.powermanga\.org/(series|read)/.',
        r'read\.yagami\.me/(series|read)/.',
        r'reader\.championscans\.com/(series|read)/.',
        r'reader\.kireicake\.com/(series|read)/.',
        r'reader\.shoujosense\.com/(series|read)/.',
        r'reader\.sensescans\.com/(series|read)/.',
        r'reader\.whiteoutscans\.com/(series|read)/.',
        r'slide\.world-three\.org/(series|read)/.',
        r'manga\.animefrontline\.com/(series|read)/.',
        r'reader\.s2smanga\.com/(series|read)/.',
        r'reader\.seaotterscans\.com/(series|read)/.',
        r'reader\.seaotterscans\.com/(series|read)/.',
        r'reader\.idkscans\.com/(series|read)/.',
        r'reader\.thecatscans\.com/(series|read)/.',
        r'reader\.deathtollscans\.net/(series|read)/.',
        r'lector\.ytnofan\.com/(series|read)/.',
        r'reader\.jokerfansub\.com/(series|read)/.',
        r'lector\.patyscans\.com/(series|read)/.',
        r'truecolorsscans\.miocio\.org/(series|read)/.',
    ],
    'ravens_scans_com': [
        r'ravens-scans\.com(/lector)?/(serie/|read/).',
    ],
    'raw_senmanga_com': [
        r'raw\.senmanga\.com/.',
    ],
    'rawdevart_com': [
        r'rawdevart\.com/manga/.',
    ],
    'read_egscans_com': [
        r'read.egscans.com/.',
    ],
    'readcomicbooksonline_org': [
        r'readcomicbooksonline\.net/.',
        r'readcomicbooksonline\.org/.',
    ],
    'readhentaimanga_com': [
        r'readhentaimanga\.com/.',
    ],
    'readcomiconline_to': [
        r'readcomiconline\.to/Comic/.',
    ],
    'readmanga_me': [
        r'readmanga\.me/.',
    ],
    'readmanga_eu': [
        r'readmanga\.eu/manga/\d+/.',
    ],
    'readmng_com': [
        r'readmng\.com/.',
    ],
    'readms_net': [
        r'readms\.net/(r|manga)/.',
    ],
    'santosfansub_com': [
        r'santosfansub\.com/Slide/.',
    ],
    'selfmanga_ru': [
        r'selfmanga\.ru/.',
    ],
    'senmanga_com': [
        r'senmanga\.com/.',
    ],
    'shakai_ru': [
        r'shakai\.ru/manga.*?/\d',
    ],
    'shogakukan_co_jp': [
        r'shogakukan\.co\.jp/books/\d',
        r'shogakukan\.co\.jp/magazines/series/\d',
    ],
    'shogakukan_tameshiyo_me': [
        r'shogakukan\.tameshiyo\.me/\d',
    ],
    'somanga_net': [
        r'somanga\.net/(leitor|manga)/.',
    ],
    'subapics_com': [
        r'subapics\.com/manga/.',
        r'subapics\.com/.+-chapter-',
        r'mangakita\.net/manga/.',
        r'mangakita\.net/.+-chapter-',
        r'komikstation\.com/manga/.',
        r'komikstation\.com/.+-chapter-',
        r'mangavy\.com/manga/.',
        r'mangavy\.com/.+-chapter-',
    ],
    'sunday_webry_com': [
        r'sunday-webry\.com/series/\d',
    ],
    'taadd_com': [
        r'taadd\.com/(book|chapter)/.',
    ],
    'tapas_io': [
        r'tapas.io/episode/\d',
        r'tapas.io/series/\w',
    ],
    'tenmanga_com': [
        r'tenmanga\.com/(book|chapter)/.',
    ],
    'tonarinoyj_jp': [
        r'tonarinoyj.jp/episode/.',
    ],
    'triplesevenscans_com': [
        r'triplesevenscans\.com/reader/(series|read)/.',
    ],
    'truyen_vnsharing_site': [
        r'truyen\.vnsharing\.site/index/read/.',
    ],
    'truyentranhtuan_com': [
        r'truyentranhtuan.com/.',
    ],
    'tsumino_com': [
        r'tsumino.com/Book/Info/\d',
        r'tsumino.com/Read/View/\d',
    ],
    'tumangaonline_com': [
        r'tumangaonline\.com/.',
    ],
    'unionmangas_net': [
        r'unionmangas\.(net|cc)/(leitor|manga)/.',
    ],
    # 'viz_com': [r'viz\.com/shonenjump/chapters/.',],
    'webtoons_com': [
        r'webtoons\.com/[^/]+/[^/]+/[^/]+',
    ],
    'webtoontr_com': [
        r'webtoontr.com/_/.',
    ],
    'wiemanga_com': [
        r'wiemanga\.com/(manga|chapter)/.',
    ],
    'wmanga_ru': [
        r'wmanga\.ru/starter/manga_.',
    ],
    'zingbox_me': [
        r'zingbox\.me/.',
    ],
    'zip_read_com': [
        r'zip-read\.com/.',
    ],
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
