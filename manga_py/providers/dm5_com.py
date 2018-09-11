from urllib.parse import quote_plus

import execjs

from manga_py.fs import is_file
from manga_py.provider import Provider
from .helpers.std import Std


class Dm5Com(Provider, Std):
    def get_chapter_index(self) -> str:
        re = self.re.compile(r'[^\d+](\d+)')
        return re.search(self.chapter[1]).group(1)

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

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        self._storage['referer'] = self.chapter[0]
        _path, idx, _url = self._save_file_params_helper(url, idx)

        if not is_file(_path):
            self.http(True).download_file(_url, _path, idx)
        callable(callback) and callback()
        self.after_file_save(_path, idx)
        self._archive.lazy_add(_path)
        return _path

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

    def chapter_for_json(self):
        return self.chapter[0]


main = Dm5Com
