import re

providers_list = {
    '3asq_info': [
        r'3asq\.info/.',
    ],
    # '8muses_com': [
    #     r'8muses\.com/comics/album/.',
    # ],
    'ac_qq_com': [
        r'ac\.qq\.com/Comic.+?/id/\d',
    ],
    'acomics_ru': [
        r'acomics\.ru/~.',
    ],
    'adulto_seinagi_org': [
        r'adulto\.seinagi\.org/(series|read)/.',
        r'xanime-seduccion\.com/(series|read)/.',
        r'twistedhelscans\.com/(series|read)/.',
        r'reader\.evilflowers\.com/(series|read)/.',
    ],
    'allhentai_ru': [
        r'allhentai\.ru/.',
    ],
    'animextremist_com': [
        r'animextremist\.com/mangas-online/.',
    ],
    'antisensescans_com': [
        r'antisensescans\.com/online/(series|read)/.',
    ],
    'asmhentai_com': [
        r'asmhentai\.com/(g|gallery)/\d',
    ],
    'atfbooru_ninja': [
        r'atfbooru\.ninja/posts.',
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
    'bns_shounen_ai_net': [
        r'bns\.shounen-ai\.net/read/(series|read)/.',
    ],
    'boredomsociety_xyz': [
        r'boredomsociety\.xyz/(titles/info|reader)/\d',
    ],
    'cdmnet_com_br': [
        r'cdmnet\.com\.br/titulos/.',
    ],
    'chochox_com': [
        r'chochox\.com/.',
    ],
    'choutensei_260mb_net': [
        r'choutensei\.260mb\.net/(series|read)/.',
    ],
    'comicextra_com': [
        r'comicextra\.com/.',
    ],
    # 'comico_co_id_content': [
    #     r'comico\.co\.id/content\?contentId=\d',
    # ],
    'comico_co_id_titles': [
        r'comico\.co\.id/titles/\d',
    ],
    'comic_webnewtype_com': [
        r'comic\.webnewtype\.com/contents/.',
    ],
    'comico_jp': [
        r'comico\.jp(?:/challenge)?/(detail|articleList).+titleNo.',
    ],
    'comicsandmanga_ru': [
        r'comicsandmanga\.ru/online-reading/.',
    ],
    'comicvn_net': [
        r'comicvn\.net/truyen-tranh-online/.',
    ],
    'danbooru_donmai_us': [
        r'danbooru\.donmai\.us/posts.',
    ],
    'darkskyprojects_org': [
        r'darkskyprojects\.org/biblioteca/.',
    ],
    'dejameprobar_es': [
        r'dejameprobar\.es/slide/.',
        r'menudo-fansub\.com/slide/.',
        r'npscan\.mangaea\.net/slide/.',
        r'snf\.mangaea\.net/slide/.',
        r'yuri-ism\.net/slide/.',
    ],
    'desu_me': [
        r'desu\.me/manga/.',
    ],
    'digitalteam1_altervista_org': [
        r'digitalteam1\.altervista\.org/reader/read/.',
    ],
    # 'dm5_com': [
    #     r'dm5\.com/manhua-.',
    # ],
    'doujins_com': [
        r'doujins\.com/gallery/.',
        r'doujin-moe\.us/gallery/.',
    ],
    'e_hentai_org': [
        r'e-hentai\.org/g/\d',
    ],
    'exhentai_org': [
        r'exhentai\.org/g/\d',
    ],
    'fanfox_net': [
        r'fanfox\.net/manga/.',
    ],
    'freeadultcomix_com': [
        r'freeadultcomix\.com/.',
    ],
    'freemanga_to': [
        r'freemanga\.to/(manga|chapter)/.',
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
    'hatigarmscans_eu': [
        r'hatigarmscans\.eu/hs/(series|read).',
        r'hatigarmscans\.net/hs/(series|read).',
        r'hatigarmscans\.net/manga/.',
    ],
    'heavenmanga_biz': [
        r'heavenmanga\.\w+/.',
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
    'hentai_image_com': [
        r'hentai-image\.com/image/.',
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
    'hgamecg_com': [
        r'hgamecg\.com/index/category/\d',
    ],
    'hitmanga_eu': [
        r'hitmanga\.eu/.',
        r'mymanga\.io/.',
    ],
    'hocvientruyentranh_com': [
        r'hocvientruyentranh\.com/(manga|chapter)/.',
    ],
    'hoducomics_com': [
        r'hoducomics\.com/webtoon/list/\d',
        r'hodu1\.com/webtoon/list/\d',
    ],
    'hotchocolatescans_com': [
        r'hotchocolatescans\.com/fs/(series|read)/.',
        r'mangaichiscans\.mokkori\.fr/fs/(series|read)/.',
        r'taptaptaptaptap\.net/fs/(series|read)/.',
    ],
    'riceballicious_info': [
        r'riceballicious\.info/fs/reader/(series|read)/.',
    ],
    'rocaca_com': [
        r'rocaca\.com/manga/.',
    ],
    'inmanga_com': [
        r'inmanga\.com/ver/manga/.',
    ],
    'japscan_com': [
        r'japscan\.cc/.',
    ],
    'jurnalu_ru': [
        r'jurnalu\.ru/online-reading/.',
    ],
    'kissmanga_com': [
        r'kissmanga\.com/Manga/.',
    ],
    'komikcast_com': [
        r'komikcast\.com/.',
    ],
    'komikid_com': [
        r'komikid\.com/manga/.',
        r'mangazuki\.co/manga/.',
        r'mangaforest\.com/manga/.',
        r'mangadenizi\.com/.',
        r'mangadoor\.com/manga/.',
        r'manga\.fascans\.com/manga/.',
        r'mangadesu\.net/manga/.',
        r'mangahis\.com/manga/.',
        r'cmreader\.info/manga/.',
        r'rawmangaupdate\.com/manga/.',
        r'mangaraw\.online/manga/.',
        r'manhua-tr\.com/manga/.',
        r'manga-v2\.mangavadisi\.org/manga/.',
        r'universoyuri\.com/manga/.',
        r'digitalteam1\.altervista\.org/manga/.',
        r'sosscanlation\.com/manga/.',
        r'komikgue\.com/manga/.',
    ],
    'kumanga_com': [
        r'kumanga\.com/manga/\d',
    ],
    'lector_kirishimafansub_com': [
        r'lector\.kirishimafansub\.com/(lector/)?(series|read)/.',
    ],
    'leitor_net': [
        r'leitor\.net/manga/.',
    ],
    'leomanga_com': [
        r'leomanga\.com/manga/.',
    ],
    'lolibooru_moe': [
        r'lolibooru\.moe/post.',
    ],
    'lolivault_net': [
        r'lolivault\.net/online/(series|read).',
    ],
    'luscious_net': [
        r'luscious\.net/.+/album/.',
        r'luscious\.net/albums/.',
    ],
    'mangapark_org': [
        r'mangapark\.org/(series|chapter)/',   # is different!
    ],
    'mang_as': [
        r'mang\.as/manga/.',
    ],
    'manga_ae': [
        r'manga\.ae/.',
    ],
    'manga_fox_com': [
        r'manga-fox\.com/.',
        r'manga-here\.io/.',
    ],
    'manga_mexat_com': [
        r'manga\.mexat\.com/category/.',
    ],
    'manga_online_biz': [
        r'manga-online\.biz/.',
    ],
    'manga_online_com_ua': [
        r'manga-online\.com\.ua/.+html',
    ],
    'manga_room_com': [
        r'manga-room\.com/manga/.',
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
    'mangabat_com': [
        r'mangabat\.com/(manga|chapter)/.',
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
        r'hentai-chan\.me/download/.',
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
        r'manga99\.com/.',
    ],
    'mangadex_com': [
        r'mangadex\.com/(title|chapter)/.',
        r'mangadex\.org/(title|chapter)/.',
    ],
    'mangaeden_com': [
        r'mangaeden\.com/[^/]+/[^/]+-manga/.',
        r'perveden\.com/[^/]+/[^/]+-manga/.',
    ],
    'mangaforall_com': [
        r'mangaforall\.com/m/.',
    ],
    'mangafreak_net_download': [
        r'mangafreak\.net/Manga/.',
    ],
    'mangafull_org': [
        r'mangafull\.org/manga/.',
    ],
    'mangago_me': [
        r'mangago\.me/read-manga/.',
    ],
    'mangahasu_se': [
        r'mangahasu\.se/.',
    ],
    'mangahere_cc': [
        r'mangahere\.co/manga/.',
        r'mangahere\.cc/manga/.',
    ],
    'mangahi_net': [
        r'mangahi\.net/.',
    ],
    'mangaid_me': [
        r'mangaid\.co/manga/.',
        r'mangaid\.net/manga/.',
        r'mangaid\.me/manga/.',
    ],
    'mangahome_com': [
        r'mangahome\.com/manga/.',
    ],
    'mangahub_io': [
        r'mangahub\.io/(manga|chapter)/.',
        r'mangareader\.site/(manga|chapter)/.',
        r'mangakakalot\.fun/(manga|chapter)/.',
        r'mangahere\.onl/(manga|chapter)/.',
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
    'mangajinnofansub_com': [  # normal
        r'mangajinnofansub\.com/lector/(series|read)/.',
    ],
    'mangakakalot_com': [
        r'mangakakalot\.com/(manga|chapter)/.',
    ],
    'mangakatana_com': [
        r'mangakatana\.com/manga/.',
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
    'mangamew_com': [
        r'mangamew\.com/(\w+-)?manga/.',
    ],
    'mangamew_com_vn': [
        r'mangamew\.com/(\w+-)?truyen/.',
    ],
    'manganelo_com': [
        r'manganelo\.com/(manga|chapter)/.',
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
    'mangareader_xyz': [
        r'mangareader\.xyz/manga/.',
        r'mangareader\.xyz/.+?/chapter-\d',
        r'mangafox\.cc/manga/.',
        r'mangafox\.cc/.+?/chapter-\d',
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
        r'mangashiro\.net/.',
    ],
    'mangasupa_com': [
        r'mangasupa\.com/(manga|chapter)/.',
    ],
    'mangatail_com': [
        r'mangasail\.com/(manga|chapter|node|content)/.',
        r'mangasail\.co/(manga|chapter|node|content)/.',
        r'mangatail\.me/(manga|chapter|node|content)/.',
    ],
    'mangatown_com': [
        r'mangatown\.com/manga/.',
    ],
    'mangatrue_com': [
        r'mangatrue\.com/manga/.',
        r'mangaall\.com/manga/.',
    ],
    'mangawindow_net': [
        r'mangawindow\.net/(series|chapter)/\d',  # is different!
    ],
    'mangax_net': [
        r'mangax\.net/\w/.',
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
    'mymangalist_org': [
        r'mymangalist.org/(read|chapter)-',
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
    'niadd_com': [
        r'niadd\.com/manga/.',
    ],
    'nightow_net': [
        r'nightow\.net/online/\?manga=.',
    ],
    'nineanime_com': [
        r'nineanime\.com/manga/.+\.html'
    ],
    'ninemanga_com': [
        r'ninemanga\.com/(manga|chapter).',
        r'addfunny\.com/(manga|chapter).',
    ],
    'noranofansub_com': [
        r'noranofansub\.com(/lector)?/(series/|read/)?.',
    ],
    'nozominofansub_com': [  # mangazuki_co
        r'nozominofansub\.com/public(/index\.php)?/manga/.',
        r'godsrealmscan\.com/public(/index\.php)?/manga/.',
    ],
    'nude_moon_me': [
        r'nude-moon\.me/\d'
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
    'plus_comico_jp_manga': [
        r'plus\.comico\.jp/manga/\d',
    ],
    'plus_comico_jp': [
        r'plus\.comico\.jp/store/\d',
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
    'ravens_scans_com': [
        r'ravens-scans\.com(/lector)?/(serie/|read/).',
    ],
    'raw_senmanga_com': [
        r'raw\.senmanga\.com/.',
    ],
    'rawdevart_com': [
        r'rawdevart\.com/manga/.',
    ],
    'rawlh_com': [
        r'lhscan\.net/(truyen|manga|read)-.',
        r'rawqq\.com/(truyen|manga|read)-.',
        r'rawqv\.com/(truyen|manga|read)-.',
    ],
    'rawneko_com': [
        r'rawneko\.com/manga/.',
    ],
    'read_egscans_com': [
        r'read\.egscans\.com/.',
    ],
    'read_powermanga_org': [
        r'lector\.dangolinenofansub\.com/(series|read)/.',
        r'read\.powermanga\.org/(series|read)/.',
        r'read\.yagami\.me/(series|read)/.',
        r'reader\.kireicake\.com/(series|read)/.',
        r'reader\.shoujosense\.com/(series|read)/.',
        r'reader\.sensescans\.com/(series|read)/.',
        r'reader\.whiteoutscans\.com/(series|read)/.',
        r'slide\.world-three\.org/(series|read)/.',
        r'manga\.animefrontline\.com/(series|read)/.',
        r'reader\.s2smanga\.com/(series|read)/.',
        r'reader\.seaotterscans\.com/(series|read)/.',
        r'reader\.idkscans\.com/(series|read)/.',
        r'reader\.thecatscans\.com/(series|read)/.',
        r'reader\.deathtollscans\.net/(series|read)/.',
        r'lector\.ytnofan\.com/(series|read)/.',
        r'reader\.jokerfansub\.com/(series|read)/.',
        r'lector\.patyscans\.com/(series|read)/.',
        r'truecolorsscans\.miocio\.org/(series|read)/.',
        r'reader\.letitgo\.scans\.today/(series|read)/.',
        r'reader\.fos-scans\.com/(series|read)/.',
        r'reader\.serenade\.moe/(series|read)/.',
        r'reader\.vortex-scans\.com/(series|read)/.',
        r'reader\.roseliascans\.com/(series|read)/.',
        r'reader\.silentsky-scans\.net/(series|read)/.',
        r'hoshiscans\.shounen-ai\.net/(series|read)/.',
        r'digitalteamreader\.netsons\.org/(series|read)/.',
        r'reader\.manga-download\.org/(series|read)/.',
    ],
    'readcomicbooksonline_org_manga': [
        r'readcomicbooksonline\.net/manga/.',
        r'readcomicbooksonline\.org/manga/.',
    ],
    'readcomicbooksonline_org': [
        r'readcomicbooksonline\.net/.',
        r'readcomicbooksonline\.org/.',
    ],
    'reader_championscans_com': [
        r'reader\.championscans\.com/(series|read)/.',
    ],
    'reader_imangascans_org': [
        r'reader\.imangascans\.org/.',
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
    'remanga_org': [
        r'remanga\.org/manga/.',
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
    'siberowl_com': [
        r'siberowl\.com/mangas/.',
    ],
    'somanga_net': [
        r'somanga\.net/(leitor|manga)/.',
        r'somangas\.net/(leitor|manga)/.',
    ],
    'subapics_com': [
        r'subapics\.com/manga/.',
        r'subapics\.com/.+-chapter-.',
        r'mangakita\.net/manga/.',
        r'mangakita\.net/.+-chapter-.',
        r'komikstation\.com/manga/.',
        r'komikstation\.com/.+-chapter-.',
        r'mangavy\.com/manga/.',
        r'mangavy\.com/.+-chapter-.',
        r'mangakid\.net/manga/.',
        r'mangakid\.net/.+-chapter-.',
    ],
    'submanga_online': [
        r'submanga\.online/manga/.',
    ],
    'sunday_webry_com': [
        r'sunday-webry\.com/series/\d',
    ],
    'taadd_com': [
        r'taadd\.com/(book|chapter)/.',
    ],
    'tapas_io': [
        r'tapas\.io/episode/\d',
        r'tapas\.io/series/\w',
    ],
    'tenmanga_com': [
        r'tenmanga\.com/(book|chapter)/.',
    ],
    'translate_webtoons_com': [
        r'translate\.webtoons\.com/webtoonVersion\?webtoonNo.',
    ],
    'trashscanlations_com': [
        r'trashscanlations\.com/series/.',
    ],
    'tonarinoyj_jp': [
        r'tonarinoyj\.jp/episode/.',
    ],
    'toonkor_co': [
        r'toonkor\.co/.',
    ],
    'triplesevenscans_com': [
        r'triplesevenscans\.com/reader/(series|read)/.',
        r'cm-scans\.shounen-ai\.net/reader/(series|read)/.',
        r'yaoislife\.shounen-ai\.net/reader/(series|read)/.',
        r'fujoshibitches\.shounen-ai\.net/reader/(series|read)/.',
    ],
    'truyen_vnsharing_site': [
        r'truyen\.vnsharing\.site/index/read/.',
    ],
    'truyenchon_com': [
        r'truyenchon\.com/truyen/.',
        r'nettruyen\.com/truyen-tranh/.',
    ],
    'truyentranhtuan_com': [
        r'truyentranhtuan\.com/.',
    ],
    'tsumino_com': [
        r'tsumino\.com/Book/Info/\d',
        r'tsumino\.com/Read/View/\d',
    ],
    'tumangaonline_com': [
        r'tumangaonline\.com/.',
        r'tumangaonline\.me/.',
    ],
    'unionmangas_net': [
        r'unionmangas\.cc/(leitor|manga)/.',
        r'unionmangas\.net/(leitor|manga)/.',
        r'unionmangas\.site/(leitor|manga)/.',
    ],
    # 'viz_com': [r'viz\.com/shonenjump/chapters/.',],
    'web_ace_jp': [
        r'web-ace\.jp/youngaceup/contents/\d',
    ],
    'webtoon_bamtoki_com': [
        r'webtoon\.bamtoki\.com/.',
        r'webtoon\.bamtoki\.se/.',
    ],
    'webtoons_com': [
        r'webtoons\.com/[^/]+/[^/]+/.',
    ],
    'webtoontr_com': [
        r'webtoontr\.com/_/.',
    ],
    'westmanga_info': [
        r'westmanga\.info/.',
    ],
    'whitecloudpavilion_com': [
        r'whitecloudpavilion\.com/manga/free/manga/.',
    ],
    'wiemanga_com': [
        r'wiemanga\.com/(manga|chapter)/.',
    ],
    'wmanga_ru': [
        r'wmanga\.ru/starter/manga_.',
    ],
    'yande_re': [
        r'yande\.re/post.',
    ],
    'zeroscans_com': [
        r'zeroscans\.com/manga/.',
    ],
    'zingbox_me': [
        r'zingbox\.me/.',
    ],
    'zip_read_com': [
        r'zip-read\.com/.',
    ],
    'zmanga_net': [
        r'zmanga\.net/.',
    ],
}


def __check_provider(provider, url):
    items = [r'\b' + i for i in provider]
    reg = '(?:' + '|'.join(items) + ')'
    return re.search(reg, url)


def get_provider(url):
    fromlist = 'manga_py.providers'
    for i in providers_list:
        if __check_provider(providers_list[i], url):
            provider = __import__('{}.{}'.format(fromlist, i), fromlist=[fromlist])
            return provider.main
    return False
