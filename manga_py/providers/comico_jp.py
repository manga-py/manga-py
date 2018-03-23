from manga_py.provider import Provider
from .helpers.std import Std


class ComicoJp(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.chapter_id)

    def get_chapter_index(self) -> str:
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
        name = self.html_fromstring(self.get_url(), 'title', 0).text_content()
        return name[:name.rfind('|')].strip(' \n\t\r')

    def get_chapters(self):
        # TODO: see i['freeFlg'] Y = true, W = false #19
        items = [i['articleDetailUrl'] for i in self.content if i['freeFlg'] == 'Y']
        self.log('Free chapters count: %d' % len(items))
        return items[::-1]

    def get_files(self):
        items = self.html_fromstring(self.chapter, '.comic-image._comicImage > img.comic-image__image')
        return [i.get('src') for i in items]

    def get_cover(self):
        pass


main = ComicoJp
