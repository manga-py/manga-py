from src.provider import Provider


class MangabbCo(Provider):

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self.get_chapter_index())

    def get_chapter_index(self) -> str:
        chapter = self.get_current_chapter()
        idx = chapter.rfind('/chapter-')
        return chapter[1 + idx:]

    def get_main_content(self):
        url = '{}/manga/{}'.format(self.get_domain(), self.get_manga_name())
        result = self.html_fromstring(url, '#chapters a')
        return result[0].get('href') if len(result) else False

    def get_manga_name(self) -> str:
        return self.re.search(r'\.co/(?:manga/)?([^/]+)', self.get_url()).group(1)

    def get_chapters(self):
        content = self.get_storage_content()
        if not content:
            return []
        selector = '#asset_1 select.chapter_select > option'
        result = self.html_fromstring(content, selector)
        return [i.get('value') for i in result[::-1]]

    @staticmethod
    def __get_img(parser):
        return parser.cssselect('#manga_viewer > a > img')[0].get('src')

    @staticmethod
    def _img_lifehack1(img, pages_list, images):
        n = 1
        for i in pages_list:
            n += 1
            images.append('{}{}{}'.format(img[0], n, img[1]))

    def _img_lifehack2(self, pages_list, images):
        for page in pages_list:
            parser = self.html_fromstring(page)
            images.append(self.__get_img(parser))

    def get_files(self):
        parser = self.html_fromstring(self.get_current_chapter(), '#body', 0)
        result = parser.cssselect('#asset_2 select.page_select option + option')
        pages_list = [i.get('value') for i in result]
        _first_image = self.__get_img(parser)
        images = [_first_image]

        img = self.re.search(r'(.+/)\d(\.\w+)', _first_image)
        if img:  # livehack
            self._img_lifehack1(img.groups(), pages_list, images)
        else:
            self._img_lifehack2(pages_list, images)

        return images


main = MangabbCo
