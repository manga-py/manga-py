from urllib.parse import quote_plus
from manga_py.provider import Provider
from .helpers.std import Std
import execjs


class Dm5Com(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        re = self.re.compile(r'[^\d+](\d+)')
        return re.search(self.chapter[1]).group(1)
        pass

    def get_main_content(self):
        content = self._storage.get('main_content', None)
        if content is None:
            if self.get_url().find('/manhua-'):
                # normal url
                name = self._get_name('/manhua-([^/]+)')
            else:
                # chapter url
                selector = '.title .right-arrow > a'
                name = self.html_fromstring(self.get_url(), selector, 0)
                name = self._get_name('/manhua-([^/]+)', name.get('href'))
            content = self.http_get('{}/manhua-{}/'.format(
                self.domain,
                name
            ))
        return content

    def get_manga_name(self) -> str:

        # a = r"""eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('b 8(){1 4=3;1 a=\'9\';1 7="g://h-k-e-j-5.c.f/5/p/3";1 2=["/o.6","/q.6"];l(1 i=0;i<2.m;i++){2[i]=7+2[i]+\'?4=3&a=9\'}n 2}1 d;d=8();',27,27,'|var|pvalue|115710|cid|10|jpg|pix|dm5imagefun|2ebb01b581e29b598ad616275b9cb866|key|function|cdndm5||250|com|http|manhua1021||150|104|for|length|return|1_1557|9404|2_3610'.split('|'),0,{}))"""
        # print(execjs.eval(a))
        # exit()

        title = self.text_content(self.content, '.info .title')
        if title:
            return title
        re = self.re.search('/manhua-([^/]+)', self.get_url())
        return re.group(1)

    def get_chapters(self):
        items = self._elements('ul.detail-list-select')
        if not items:
            return []
        items = items[0].cssselect('li > a')
        n = self.http().normalize_uri
        return [(n(i.get('href')), i.text_content()) for i in items]

    def get_files(self):  # fixme
        content = self.http_get(self.chapter[0])
        parser = self.document_fromstring(content)
        pages = parser.cssselect('.chapterpager a')
        if pages:
            pages = int(pages[-1].text_content().strip())
        else:
            pages = 1
        s = lambda k: self.re.search(r'%s\s*=[\s"]*(.+?)[\s"]*;' % k, content).group(1)
        key = parser.cssselect('#dm5_key')[0].get('value')
        cid = s(r'\bDM5_CID')
        mid = s(r'\bDM5_MID')
        sign = s(r'\bDM5_VIEWSIGN')
        sign_dt = quote_plus(s(r'\bDM5_VIEWSIGN_DT'))
        chapter_idx = self.re.search(r'/(m\d+)', self.chapter[0]).group(1)
        url = '{}/{}/chapterfun.ashx?cid={}&page={}&key={}&language=1&gtk=6&_cid={}&_mid={}&_dt={}&_sign={}'
        items = []
        for page in range(pages):
            data = self.http_get(url.format(
                self.domain, chapter_idx,
                cid, page + 1, key, cid,
                mid, sign_dt, sign,
            ), headers=self._get_headers())
            item_url = execjs.eval(data)
            if item_url:
                items += item_url
        return items

    @staticmethod
    def _get_headers():
        return {'Cache-mode': 'no-cache', 'X-Requested-With': 'XMLHttpRequest'}

    def get_cover(self) -> str:
        return self._cover_from_content('.banner_detail_form .cover > img')

    def book_meta(self) -> dict:
        rating = self.text_content(self.content, '.right .score', 0)
        rating = self.re.search(r'(\d\d?\.\d)', rating).group(1)
        author = self.text_content(self.content, '.banner_detail_form .info .subtitle a')
        anno = self.text_content(self.content, '.banner_detail_form .info .content')
        return {
            'author': author,
            'title': self.get_manga_name(),
            'annotation': anno,
            'keywords': str,
            'cover': self.get_cover(),
            'rating': rating,
        }


main = Dm5Com
