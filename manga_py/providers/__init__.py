import re
import importlib

providers_list = {
    '1stkissmanga_com': [
        r'1stkissmanga\.com/manga/.',
    ],
    '_3asq_org': [
        r'3asq\.org/.',
    ],
    '7sama_com': [
        r'7sama\.com/manga/.',
    ],
    '18comic_org': [
        r'18comic\.org/album/\d'
    ],
    'ac_qq_com': [
        r'ac\.qq\.com/Comic.+?/id/\d',
    ],
    'acomics_ru': [
        r'acomics\.ru/~.',
    ],
    'adulto_seinagi_org': [
        r'xanime-seduccion\.com/(series|read)/.',
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
    'bato_to': [
        r'bato\.to/series/\d',
        r'mangawindow\.net/series/\d',
    ],
    'blogtruyen_com': [
        r'blogtruyen\.com/.',
    ],
    'cdmnet_com_br': [
        r'cdmnet\.com\.br/titulos/.',
        r'centraldemangas.online/titulos/.'
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
        r'comico\.jp/(?:challenge/)?(detail|articleList).+titleNo.',
    ],
    'comicvn_net': [
        r'comicvn\.net/truyen-tranh-online/.',
    ],
    'cycomi_com': [
        r'cycomi\.com/fw/cycomibrowser/chapter/title/\d',
    ],
    'danbooru_donmai_us': [
        r'danbooru\.donmai\.us/posts.',
    ],
    'darkskyprojects_org': [
        r'darkskyprojects\.org/biblioteca/.',
    ],
    'dejameprobar_es': [
        r'menudo-fansub\.com/slide/.',
        r'yuri-ism\.net/slide/.',
    ],
    'desu_me': [
        r'desu\.me/manga/.',
    ],
    'doujins_com': [
        r'doujins\.com/hentai-manga/.',
        r'doujins\.com/gallery/.',
        r'doujin-moe\.us/gallery/.',
    ],
    'e_hentai_org': [
        r'e-hentai\.org/g/\d',
    ],
    'fanfox_net': [
        r'fanfox\.net/manga/.',
    ],
    'funmanga_com': [
        r'funmanga\.com/.',
    ],
    'gmanga_me': [
        r'gmanga\.me/mangas/.',
    ],
    'gomanga_co': [
        r'kobato\.hologfx\.com/reader/.',
    ],
    'helveticascans_com': [
        r'helveticascans\.com/r/(series|read)/.',
    ],
    'heavenmanga_biz': [
        r'heavenmanga\.com/.',
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
        r'hentai-img\.com/image/.',
        r'hentai-image\.com/image/.',
    ],
    'hentaihand_com': [
        r'hentaihand\.com/comic/\d',
    ],
    'hentaifox_com': [
        r'hentaifox\.com/.',
    ],
    'hentaihere_com': [
        r'hentaihere\.com/m/.',
    ],
    'hentailxx_com': [
        r'hentailxx\.com/story/view\.php\?id=\d'
    ],
    'hentainexus_com': [
        r'hentainexus\.com/(read|view)/\d'
    ],
    'hentaiporns_net': [
        r'hentaiporns\.net/.'
    ],
    'hentairead_com': [
        r'hentairead\.com/.',
    ],
    'hentaivn_net': [
        r'hentaivn\.net/\d+-doc-.',
    ],
    'hitomi_la': [
        r'hitomi\.la/(galleries|reader)/.',
    ],
    'hgamecg_com': [
        r'hgamecg\.com/index/category/\d',
    ],
    'hiperdex_com': [
        r'hiperdex\.com/manga/.',
    ],
    'hitmanga_eu': [
        r'mymanga\.io/.',
    ],
    'hocvientruyentranh_com': [
        r'hocvientruyentranh\.com/(manga|chapter)/.',
    ],
    'hotchocolatescans_com': [
        r'taptaptaptaptap\.net/fs/(series|read)/.',
    ],
    'rocaca_com': [
        r'rocaca\.com/manga/.',
    ],
    'inmanga_com': [
        r'inmanga\.com/ver/manga/.',
    ],
    'isekaiscan_com': [
        r'mangadods\.com/manga/.',
        r'mangaus\.xyz/manga/.',
        r'nitroscans\.com/manga/.',
        r's2manga\.com/manga/.',
        r'manytoon\.com/manga/.',
        r'socialweebs\.in/manga/.',
        r'toongod\.com/manga/.',
        r'mangakik\.com/manga/.',
        r'kissmanga\.in/manga/.',
        r'soloscanlation\.site/manga/.',
        r'manhuaes\.com/manga/.',
        r'manhuasy\.com/manga/.',
        r'grazescans\.com/manga/.',
        r'sixiangscans\.com/manga/.',
        r'toonpoint\.com/manga/.',
        r'mangasco\.com/manga/.',
        r'lilymanga\.com/manga/.',
        r'mangacultivator\.com/manga/.',
        r'365manga\.com/manga/.',
        r'freewebtooncoins\.com/manga/.',
        r'mangatoo\.com/manga/.',
        r'webtoon\.xyz/manga/.',
        r'mangaweebs\.in/manga/.',
        r'manhuabox.net/manga/.',
        r'mangaread\.org/manga/.',
        r'manga1st\.com/manga/.',
        r'aloalivn\.com/manga/.',
        r'skscans\.com/manga/.',
        r'imperfectcomic\.com/manga/.',
        r'astrallibrary\.net/manga/.',
        r'manhwa\.live/manga/.',
        r'mangasy\.com/manga/.',
        r'woopread\.com/manga/.',
        r'allporncomic\.com/manga/.',
        r'mangarockteam\.com/manga/.',
        r'kisekimanga\.com/manga/.',
        r'mixedmanga\.com/manga/.',
        r'mangaturf\.com/manga/.',
        r'manganelo\.link/manga/.',
        r'webtoonily\.com/manga/.',
        r'mangabin\.com/manga/.',
        r'vanguardbun\.com/manga/.',
        r'webnovel\.live/manga/.',
        r'mangarocky\.com/manga/.',
        r'catonhead\.com/manga/.',
        r'voidscans\.com/manga/.',
        r'mm-scans\.com/manga/.',
        r'shoujohearts\.com/manga/.',
        r'wuxiaworld\.site/manga/.',
        r'ntsvoidscans\.com/manga/.',
        r'toonily\.com/manga/.',
        r'manhuasworld\.com/manga/.',
        r'mangatx\.com/manga/.',
        r'manhwatop\.com/manga/.',
        r'manga18fx\.com/manga/.',
        r'randomtranslations\.com/manga/.',
        r'pmscans\.com/manga/.',
        r'mangazukinew\.online/manga/.',
        r'mangahentai\.me/manga/.',
        r'mangachill\.com/manga/.',
        r'manga347\.com/manga/.',
        r'mangaeffect\.com/manga/.',
        r'manga1st\.online/manga/.',
        r'shieldmanga\.club/manga/.',
        r'zinmanga\.com/manga/.',
        r'en.ruyamanga\.com/manga/.',
        r'manhuaga\.com/manga/.',
        r'miraclescans\.com/manga/.',
        r'manhuas\.net/manga/.',
        r'twilightscans\.com/manga/.',
        r'manga3s\.com/manga/.',
        r'skymanga\.co/manga/.',
        r'leviatanscans\.com/manga/.',
        r'isekaiscanmanga\.com/manga/.',
        r'itsyourightmanhua\.com/manga/.',
        r'1stkissmanhua\.com/manga/.',
        r'isekaiscan\.com/manga/.',
        r'reader.decadencescans\.com/manga/.',
        r'manhwa\.club/manga/.',
        r'manytoon\.me/manga/.',
        r'nekoscan\.com/manga/.',
        r'disasterscans\.com/manga/.',
        r'topmanhua\.com/manga/.',
        r'mangakiss\.org/manga/.',
        r'animangaes\.com/manga/.',
        r'einherjarscans\.space/manga/.',
        r'porncomixonline\.net/manga/.',
        r'mortalsgroove\.com/manga/.',
        r'milftoon\.xxx/manga/.',
        r'manhuafast\.com/manga/.',
        r'raiderscans\.com/manga/.',
        r'mangaclash\.com/manga/.',
        r'immortalupdates\.com/manga/.',
        r'aoc\.moe/manga/.',
        r'tritinia\.com/manga/.',
        r'bestmanhua\.com/manga/.',
        r'mangagreat\.com/manga/.',
        r'new.renascans\.com/manga/.',
        r'manhuaplus\.com/manga/.',
        r'toonily\.net/manga/.',
        r'webtoon\.uk/manga/.',
        r'nazarickscans\.com/manga/.',
        r'herozscans\.com/manga/.',
        r'mangalord\.com/manga/.',
        r'hscans\.com/manga/.',
        r'boyslove\.me/manga/.',
        r'heromanhua\.com/manga/.',
        r'mangabob\.com/manga/.',
        r'wescans\.xyz/manga/.',
        r'arangscans\.com/manga/.',
        r'mangaroma\.com/manga/.',
        r'readmanhua\.net/manga/.',
        r'neatmanga\.com/manga/.',
        r'manga18\.fun/manga/.',
        r'nightcomic\.com/manga/.',
        r'comickiba\.com/manga/.',
        r'manganine\.com/manga/.',
        r'primemanga\.com/manga/.',
        r'manhuaus\.com/manga/.',
        r'mangaread\.co/manga/.',
        r'onmanga\.com/manga/.',
        r'painfulnightzscan\.com/manga/.',
        r'manga68\.com/manga/.',
        r'sleepytranslations\.com/manga/.',
        r'manhwahentai\.me/manga/.',
        r'jjutsuscans\.com/manga/.',
        r'mysticalmerries\.com/manga/.',
        r'mangarave\.com/manga/.',
        r'thetopcomic\.com/manga/.',
    ],
    # 'jaiminisbox_com': [
    #     r'jaiminisbox\.com/reader/series/.',
    # ],
    'jaiminisbox_net': [
        r'jaiminisbox\.net/manga/.',
    ],
    'japscan_com': [
        r'japscan\.(cc|com|co|to|se)/.',
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
        r'mangadoor\.com/manga/.',
        r'cmreader\.info/manga/.',
        r'rawmangaupdate\.com/manga/.',
        r'manga-v2\.mangavadisi\.org/manga/.',
        r'universoyuri\.com/manga/.',
        r'digitalteam1\.altervista\.org/manga/.',
        r'komikgue\.com/manga/.',
        r'onma\.me/manga/.',
    ],
    'kumanga_com': [
        r'kumanga\.com/manga/\d',
    ],
    'leitor_net': [
        r'leitor\.net/manga/.',
    ],
    'leviatanscans_com': [
        r'leviatanscans\.com/comics/\d',
        r'es\.leviatanscans\.com/comics/\d',
        r'krakenscans\.com/comics/\d',
        r'skscans\.com/comics/\d',
    ],
    'lhtranslation_com': [
        r'read\.lhtranslation\.com/(truyen|manga)-.',
        r'lhtranslation\.net/(truyen|manga)-.',
    ],
    'littlexgarden_com': [
        r'littlexgarden\.com/(?!mangas|infos|likes|notifications)'
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
    'manga41_com': [
        r'manga41\.com/manga/.',
    ],
    'manga_ae': [
        r'mangaae\.com/.',
    ],
    'manga_mexat_com': [
        r'manga\.mexat\.com/category/.',
    ],
    'manga_online_biz': [
        r'manga-online\.biz/.',
    ],
    'manga_tube_me': [
        r'manga-tube\.me/series/.',
    ],
    'mangaarabteam_com': [
        r'mangaarabteam\.com/.',
    ],
    'manga_tr_com': [
        r'manga-tr\.com/(manga|id)-.',
    ],
    'mangabat_com': [
        r'mangabat\.com/(manga|chapter)/.',
        r'mangabat\.com/read-.',
    ],
    'mangabox_me': [
        r'mangabox\.me/reader/.',
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
    'mangadex_org_v2': [
        r'mangadex\.org/(manga|title)/.',
    ],
    'mangaeden_com': [
        r'mangaeden\.com/[^/]+/[^/]+-manga/.',
        r'perveden\.com/[^/]+/[^/]+-manga/.',
    ],
    'mangafreak_net_download': [
        r'mangafreak\.net/Manga/.',
    ],
    'mangahere_cc': [
        r'mangahere\.cc/manga/.',
    ],
    'mangaid_me': [
        r'bacamanga\.co/manga/.',
    ],
    'mangahome_com': [
        r'mangahome\.com/manga/.',
    ],
    'mangahub_io': [
        r'mangahub\.io/(manga|chapter)/.',
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
    'mangakakalot_com': [
        r'mangakakalot\.com/manga/.',
        r'mangakakalot\.com/read-.',
    ],
    'mangakatana_com': [
        r'mangakatana\.com/manga/.',
    ],
    'mangakomi_com': [
        r'mangakomi\.com/manga/.',
    ],
    'mangaku_web_id': [
        r'mangaku\.in/.',
        r'mangaku\.pro/.',
    ],
    'mangalib_me': [
        r'mangalib\.me/.',
    ],
    'mangalife_us': [
        # r'mangalife\.us/(read-online|manga)/.',  # site dead
        r'manga4life\.com/(read-online|manga)/.',
    ],
    'mangamew_com': [
        r'mangamew\.com/(\w+-)?manga/.',
    ],
    'mangamew_com_vn': [
        r'mangamew\.com/(\w+-)?truyen/.',
    ],
    'manganato_com': [
        r'manganato\.com/manga-',
        r'readmanganato\.com/manga-',
    ],
    'manganelo_com': [
        r'manganelo\.com/(manga|chapter)/.',
    ],
    'manganelos_com': [
        r'manganelos\.com/manga/.',
    ],
    'mangaonline_com_br': [
        r'mangaonline\.com\.br/.',
    ],
    'mangapanda_onl': [
        r'mangapanda\.onl/manga/.',
        r'mangareader\.site/manga/.',
    ],
    'mangapark_me': [
        r'mangapark\.net/manga/.',
    ],
    'mangareader_cc': [
        r'mangareader\.cc/manga/.',
    ],
    'mangareader_net': [
        r'mangareader\.net/.',
    ],
    'mangarussia_com': [
        r'mangarussia\.com/(manga|chapter)/.',
    ],
    'mangaseeonline_us': [
        r'mangasee123\.com/(read-online|manga)/.',
    ],
    'mangashiro_net': [
        r'mangashiro\.net/.',
    ],
    'mangasushi_net': [
        r'mangasushi\.net/manga/.',
        r'asurascans\.com/manga/.',
    ],
    'mangatail_com': [
        r'mangatail\.me/(manga|chapter|node|content)/.',
    ],
    'mangatown_com': [
        r'mangatown\.com/manga/.',
    ],
    'mangawindow_net': [
        r'mangawindow\.net/(series|chapter)/\d',  # is different!
    ],
    'mangazuki_me': [
        r'mangazuki\.me/manga/.',
        r'mangazuki\.online/mangas/.',
    ],
    'manhuagui_com': [
        r'manhuagui\.com/comic/\d',
    ],
    'manhuatai_com': [
        r'manhuatai\.com/.',
    ],
    'manhwa18_net': [
        r'manhwa18\.net/manga-.',
    ],
    'manhwa_club': [
        r'manhwa\.club/manhwa/.',
    ],
    'manhwareader_com': [
        r'manhwareader\.com/manga/.',
    ],
    'merakiscans_com': [
        r'merakiscans\.com/manga/.',
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
        r'godsrealmscan\.com/public(/index\.php)?/manga/.',
    ],
    'otakusmash_com': [
        r'mentalmanga\.com/.'
        r'omgbeaupeep\.com/comics/.',
    ],
    'otscans_com': [
        r'otscans\.com/foolslide/(series|read)/.',
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
        r'rawdevart\.com/comic/.',
    ],
    'rawlh_com': [
        r'lhscan\.net/(truyen|manga|read)-.',
        r'kisslove\.net/(truyen|manga|read)-.',
        r'loveheaven\.net/(truyen|manga|read)-.',
    ],
    'read_egscans_com': [
        r'read\.egscans\.com/.',
    ],
    'read_powermanga_org': [
        r'read\.powermanga\.org/(series|read)/.',
        r'reader\.kireicake\.com/(series|read)/.',
        r'slide\.world-three\.org/(series|read)/.',
        r'reader\.thecatscans\.com/(series|read)/.',
        r'reader\.deathtollscans\.net/(series|read)/.',
        r'reader\.jokerfansub\.com/(series|read)/.',
        r'lector\.patyscans\.com/(series|read)/.',
        r'truecolorsscans\.miocio\.org/(series|read)/.',
        r'reader\.letitgo\.scans\.today/(series|read)/.',
        r'reader\.fos-scans\.com/(series|read)/.',
        r'reader\.serenade\.moe/(series|read)/.',
        r'reader\.vortex-scans\.com/(series|read)/.',
        r'reader\.silentsky-scans\.net/(series|read)/.',
        r'reader\.manga-download\.org/(series|read)/.',
    ],
    'read_ptscans_com': [
        r'read\.ptscans\.com/series/.'
    ],
    'read_yagami_me': [
        r'read\.yagami\.me/series/\w',
    ],
    'comicpunch_net_manga': [
        r'comicpunch\.net/asiancomics/.',
    ],
    'comicpunch_net': [
        r'comicpunch\.net/.',
    ],
    'readcomiconline_to': [
        r'readcomiconline\.to/Comic/.',
    ],
    'readcomicsonline_ru': [
        r'readcomicsonline\.ru/comic/.',
    ],
    'readmanga_me': [
        r'readmanga\.live/.',
        r'mintmanga\.live/.',
        r'selfmanga\.ru/.',
    ],
    'readmng_com': [
        r'readmng\.com/.',
    ],
    # todo #266
    'remanga_org': [
        r'remanga\.org/manga/.',
    ],
    'santosfansub_com': [
        r'santosfansub\.com/Slide/.',
    ],
    'senmanga_com': [
        r'senmanga\.com/.',
    ],
    'serimanga_com': [
        r'serimanga.com/manga/.'
    ],
    'shakai_ru': [
        r'shakai\.ru/manga.*?/\d',
    ],
    'shogakukan_co_jp': [
        r'shogakukan\.co\.jp/books/\d',
        r'shogakukan\.co\.jp/magazines/series/\d',
    ],
    'siberowl_com': [
        r'siberowl\.com/mangas/.',
    ],
    'sleepypandascans_co': [
        r'sleepypandascans\.co/(Series|Reader)/.',
    ],
    'subapics_com': [
        r'mangakita\.net/manga/.',
        r'mangakita\.net/.+-chapter-.',
        r'komikstation\.com/manga/.',
        r'komikstation\.com/.+-chapter-.',
        r'mangavy\.com/manga/.',
        r'mangavy\.com/.+-chapter-.',
        r'asurascans\.com/comics/.',
        r'asurascans\.com/.+-chapter-.',
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
    'tenmanga_com': [
        r'tenmanga\.com/(book|chapter)/.',
    ],
    'translate_webtoons_com': [
        r'translate\.webtoons\.com/webtoonVersion\?webtoonNo.',
    ],
    'tonarinoyj_jp': [
        r'tonarinoyj\.jp/episode/.',
    ],
    'triplesevenscans_com': [
        r'sensescans\.com/reader/(series|read)/.',
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
    'viz_com': [
        r'viz\.com/shonenjump/chapters/.',
    ],
    'web_ace_jp': [
        r'web-ace\.jp/youngaceup/contents/\d',
    ],
    'webtoons_com': [
        r'webtoons\.com/[^/]+/[^/]+/.',
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
        r'zeroscans\.com/comics/.',
        r'reaperscans\.com/comics/.',
        r'secretscan\.co/comics/.',
        r'lynxscans\.com/comics/.',
        r'kkjscans\.co/comics/.',
        r'edelgardescans\.com/comics/.',
        r'hunlight-scans\.info/comics/.',
        r'hatigarmscanz\.net/comics/.',
        r'the-nonames\.com/comics/.',
        r'methodscans\.com/comics/.',
        r'leviatanscans\.com/comics/.'
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
            provider = importlib.import_module('%s.%s' % (fromlist, i))
            return provider.main
    return False
