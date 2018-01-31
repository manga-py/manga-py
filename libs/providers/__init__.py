import re


"""
TODO:


class Reg(object):
  def __init__(self, domain):
    self.domain = domain

class RegA(Registrar):
  @classmethod
  def is_reg_for(cls, domain):
    return domain == 'foo.com'

class RegB(Registrar):
  @classmethod
  def is_reg_for(cls, domain):
    return domain == 'bar.com'


def Domain(domain):
  for cls in Reg.__subclasses__():
    if cls.is_reg_for(domain):
      return cls(domain)
  raise ValueError


print Domain('foo.com')
print Domain('bar.com')


"""

providers_list = {
    'comicextra_com': ['comicextra\\.com/.+'],
    'comico_jp': ['comico\\.jp/(detail|articleList).+titleNo.+'],
    'comicsandmanga_ru': ['comicsandmanga\\.ru/online\\-reading/.+'],
    'desu_me': ['desu\\.me/manga/.+'],
    'funmanga_com': ['funmanga\\.com/.+'],
    'goodmanga_net': ['goodmanga\\.net/.+'],
    'inmanga_com': ['inmanga\\.com/ver/manga/.+'],
    'jurnalu_ru': ['jurnalu\\.ru/online\\-reading/.+'],
    'kissmanga_com': ['kissmanga\\.com/Manga/.+'],
    'manga_online_biz': ['manga\\-online\\.biz/.+'],
    'manga_online_com_ua': ['manga\\-online\\.com\\.ua/.+html'],
    'mangabb_co': ['mangabb\\.co/.+'],
    'mangabox_me': ['mangabox\\.me/reader/.+'],
    'mangachan_me': ['mangachan\\.me/(related|manga|download)/.+'],
    'mangaclub_ru': ['mangaclub\\.ru/.+'],
    'mangaeden_com': ['mangaeden\\.com/[^/]+/[^/]+\\-manga/.+'],
    'mangafox_la': ['mangafox\\.(me|la)/manga/.+'],
    'mngdoom_com': ['(mangadoom\\.co|mngdoom\\.com)/.+'],
    'mangago_me': ['mangago\\.me/read\\-manga/.+'],
    'mangahere_co': ['mangahere\\.(co|cc)/manga/.+'],
    'mangahome_com': ['mangahome\\.com/manga/.+'],
    'mangahub_ru': ['mangahub\\.ru/.+'],
    'mangainn_net': ['mangainn\\.net/.+'],
    'mangakakalot_com': ['mangakakalot\\.com/(manga|chapter)/.+'],
    'mangalib_me': ['mangalib\\.me/.+'],
    'mangalife_us': ['mangalife\\.us/(read\\-online|manga)/.+'],
    'mangaonline_today': ['mangaonline\\.today/.+'],
    'mangaonlinehere_com': ['mangaonlinehere\\.com/(manga\\-info|read\\-online)/.+'],
    'mangapanda_com': ['mangapanda\\.com/.+'],
    'mangapark_me': ['mangapark\\.me/manga/.+'],
    'mangareader_net': ['mangareader\\.net/.+'],
    # 'mangaroot_com': ['mangaroot\\.com/manga/.+'],
    'mangarussia_com': ['mangarussia\\.com/(manga|chapter)/.+'],
    # 'mangasaurus_com': ['mangasaurus\\.com/manga.+'],
    # 'mangasupa_com': ['mangasupa\\.com/(manga|chapter).+'],
    # 'mangatan_net': ['mangashin\\.com/(manga|chapter)', 'mangatan\\.net/(manga|chapter)'],
    # 'mangatown_com': ['mangatown\\.com/manga.+'],
    # # 'mangaz_com': ['\\.mangaz\\.com/.+'],
    # 'manhuagui_com': ['manhuagui\\.com/comic/\\d+'],
    # 'mintmanga_com': ['mintmanga\\.com/.+'],
    # 'myreadingmanga_info': ['myreadingmanga\\.info/.+'],  # with cf-protect
    # 'ninemanga_com': ['ninemanga\\.com/manga.+'],
    # # 'onemanga_com': ['onemanga\\.com/manga.+'],
    # 'read_yagami_me': ['read\\.yagami\\.me/.+'],
    # 'readcomicbooksonline_net': ['readcomicbooksonline\\.net/.+'],
    # 'readcomiconline_to': ['readcomiconline\\.to/Comic/.+'],
    'readmanga_me': ['readmanga\\.me/.+'],
    # 'readmanga_eu': ['readmanga\\.eu/manga/\d+/.+'],
    # 'readms_net': ['readms\\.net/(r|manga)/.+'],
    # 'selfmanga_ru': ['selfmanga\\.ru/.+'],
    # 'shakai_ru': ['shakai\\.ru/manga.*?/\d+'],
    # 'somanga_net': ['somanga\\.net/.+'],
    # 'taadd_com': ['taadd\\.com/(book|chapter)/.+'],
    # 'tapas_io': ['tapas\\.io/(series|episode)/.+'],
    # 'tenmanga_com': ['tenmanga\\.com/(book|chapter)/.+'],
    # 'unixmanga_nl': ['unixmanga\\.nl/onlinereading/.+\\.html'],
    # 'wmanga_ru': ['wmanga\\.ru/starter/manga_.+'],
    # 'viz_com': ['viz\\.com/shonenjump/chapters/.+'],
    # 'yaoichan_me': ['yaoichan\\.me/(manga|online).+'],
    # 'zingbox_me': ['zingbox\\.me/.+'],
    # 'zip_read_com': ['zip\\-read\\.com/.+'],
    #
    # 'otakusmash_com': ['otakusmash\\.com', 'mrsmanga\\.com', 'mentalmanga\\.com']
}


def __check_provider(provider, url):
    reg = '(' + '|'.join(provider) + ')'
    return re.search(reg, url)


def get_provider(url):
    for i in providers_list:
        if __check_provider(providers_list[i], url):
            provider = __import__('libs.providers.{}'.format(i), fromlist=['libs.providers'])
            return provider.main
    return False
