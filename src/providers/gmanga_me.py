from src.providers.gomanga_co import GoMangaCo


class GMangaMe(GoMangaCo):
    _name_re = '/mangas/([^/]+)'
    _content_str = '{}/mangas/{}'
    _chapters_selector = 'a.chapter-link'

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return 'vol_{:0>3}-{}'.format(*idx)

    def get_main_content(self):
        content = super().get_main_content()
        if content.find('data-translate="allow_5_secs"') > 0:
            self.cf_protect(self.get_url())
            content = super().get_main_content()
        return content

    def get_chapter_index(self) -> str:
        selector = '/mangas/[^/]+/(\\d+/[^/]+)'
        url = self.get_current_chapter()
        idx = self.re.search(selector, url).group(1)
        return idx.replace('/', '-')

    def _get_json_selector(self, content):
        return '1:\\salphanumSort\\((\\[.+\\])\\)'

    def get_cover(self) -> str:
        content = self.get_storage_content()
        image = self.re.search('"image"\\s?:\\s?"(.+)",', content)
        if image:
            return image.group(1)


main = GMangaMe
