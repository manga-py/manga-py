from .provider import Provider


class BatoTo(Provider):

    batoto_manga_name = ''

    def get_archive_name(self) -> str:
        return 'vol_{:0>3}'.format(self._storage['current_chapter'])

    def get_chapter_index(self) -> str:
        return str(self._storage['current_chapter'])

    def get_main_content(self):  # call once
        name = self.get_manga_name()
        return self.http_get('{}/comic/_/comics/{}'.format(self.get_domain(), name))

    def get_manga_name(self):  # call once
        if len(self.batoto_manga_name):
            return self.batoto_manga_name
        url = self.get_url()
        sharp_test = self.re.search('/reader(#[^/]+)', url)
        if sharp_test:
            sharp_params = self.__sharp_helper(url)
            print(self.http_get(sharp_params['url'], **sharp_params['params']))
            exit()
            url = self.html_fromstring(sharp_params, 'li > a[href*="/comics"]', 0).get('href')
        self.batoto_manga_name = self.re.search('/comics/([^/]+)', url).group(1)
        print(self.batoto_manga_name)
        return self.batoto_manga_name

    def get_chapters(self):  # call once
        items = self.document_fromstring(self.get_main_content(), '.chapters_list a[href*="/reader#"]')
        return [i.get('href') for i in items] if items else []

    def prepare_cookies(self):  # if site with cookie protect
        self.cf_protect(self.get_url())

    def get_files(self):  # call ever volume loop
        chapter = self.get_current_chapter()
        content = self.html_fromstring(self.__sharp_helper(chapter), '#page_select', 0)
        pages = content.cssselect('option + option')
        images = [content.cssselect('img#comic_page')[0].get('src')]
        for i in pages:
            n = 1
            i = i.get('value')
            if i.find('_'):
                n = i.split('_')[1]
            img = self.html_fromstring(self.__sharp_helper(chapter, n), 'img#comic_page', 0).get('src')
            images.append(img)
        return images

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass

    def __sharp_helper(self, url, page_index=1):
        domain = self.get_domain()
        sharp = url.split('#')[1]
        if sharp.find('_') > 0:
            sharp = sharp.split('_')[0]
        api_uri = '{}/areader?id={}&p={}'.format(domain, sharp, page_index)

        return {
            'url': api_uri,
            'params': {
                'headers': {'Referer': '{}/reader'.format(domain)}
            }
        }


main = BatoTo
