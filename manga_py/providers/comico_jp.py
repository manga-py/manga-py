from manga_py.provider import Provider
from .helpers.std import Std
from sys import stderr


class ComicoJp(Provider, Std):

    def get_chapter_index(self) -> str:
        idx = self.re.search(r'articleNo=(\d+)', self.chapter)
        if idx:
            return '{}-{}'.format(self.chapter_id, idx.group(1))
        return str(self.chapter_id)

    def get_main_content(self):
        title_no = self.re.search(r'\.jp/.+titleNo=(\d+)', self.get_url())
        if title_no:
            content = self.http_post('{}/api/getArticleList.nhn'.format(self.domain), data={
                'titleNo': title_no.group(1)
            })
            try:
                return self.json.loads(content).get('result', {}).get('list', [])
            except TypeError:
                pass
        return []

    def get_manga_name(self):
        content = self.http_get(self.get_url())
        name = self.text_content(content, 'title')
        return name[:name.rfind('|')].strip(' \n\t\r')

    def get_chapters(self):
        # TODO: see i['freeFlg'] Y = true, W = false #19
        items = [i['articleDetailUrl'] for i in self.content if i['freeFlg'] == 'Y']
        self.log('Free chapters count: %d' % len(items), file=stderr)
        return items[::-1]

    def get_files(self):
        items = self.html_fromstring(self.chapter, '.comic-image._comicImage > img.comic-image__image')
        return [i.get('src') for i in items]

    def get_cover(self):
        pass

    def book_meta(self) -> dict:
        # todo meta
        pass


main = ComicoJp
