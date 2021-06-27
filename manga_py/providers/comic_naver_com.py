from manga_py.provider import Provider
from .helpers.std import Std


class ComicNaverCom(Provider, Std):
    title_id = 0
    url_pattern = 'https://comic.naver.com/webtoon/list.nhn?titleId={}'

    def get_archive_name(self) -> str:
        return self.get_chapter_index()

    def get_chapter_index(self) -> str:
        return 'vol_{}-{}'.format(self.chapter_id, self.chapter[1])

    def get_content(self):
        return self.http_get(self.url_pattern.format(self.title_id))

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.comicinfo > .detail > h2')

    def _chapters_part(self, content: str):
        elements = self._elements('.viewList .title > a', content)
        pager = self._elements('.page > .num_page', content)

        if len(pager) == 0:
            return elements, 1

        return elements, int(self.element_text_content_full(pager[-1]))

    def get_chapters(self):
        self.log('Parse chapters, please wait...')
        chapters, max_page = self._chapters_part(self.content)
        page = 2

        while True:
            if page >= max_page:
                break

            content = self.http_get(self.url_pattern.format(f'{self.title_id}&page={page}'))
            _chapters, max_page = self._chapters_part(content)

            chapters = [*chapters, *_chapters]

            page += 1

        n = self.http().normalize_uri
        return [(n(chapter.get('href')), self.element_text_content(chapter)) for chapter in chapters]

    def get_files(self):
        parser = self.document_fromstring(self.http_get(self.chapter[0]), '#comic_view_area', 0)
        return self._images_helper(parser, '.wt_viewer > img')

    def get_cover(self) -> str:
        return self._cover_from_content('.comicinfo > .thumb > a > img')

    def chapter_for_json(self) -> str:
        return self.chapter[0]

    def prepare_cookies(self):
        self.title_id = self.re.search(r'\btitleId=(\d+)', self.get_url()).group(1)


main = ComicNaverCom
