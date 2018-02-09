from src.provider import Provider


class Comico(Provider):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self._storage['current_chapter'])

    def get_chapter_index(self) -> str:
        return str(self._storage['current_chapter'])

    def get_main_content(self):
        title_no = self.re.search(r'\.jp/.+titleNo=(\d+)', self.get_url())
        if title_no:
            content = self.http_post('{}/api/getArticleList.nhn'.format(self.get_domain()), data={
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
        items = [i['articleDetailUrl'] for i in self.get_storage_content() if i['freeFlg'] == 'Y']
        self.logger_callback('Free chapters count: %d' % len(items))
        return items[::-1]

    def get_files(self):
        items = self.html_fromstring(self.get_current_chapter(), '.comic-image._comicImage > img.comic-image__image')
        return [i.get('src') for i in items]


main = Comico
