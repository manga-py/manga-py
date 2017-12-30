from .provider import Provider


class Bulumanga(Provider):
    __temp = {}

    def get_archive_name(self):
        return self.basename(self.get_current_chapter())

    def _check_source(self, content):
        source = self.re.search('source=(\w+)', self.get_url())
        resources = self.json.loads(content)['sources']
        if source:
            source = source.group(1)
            for n, i in enumerate(resources):
                if i['source'] == source:
                    return resources[n]
        return self.quest(enumerate(resources), 'Please, select resource')

    def get_main_content(self):
        re_id = self.re.search('\bid=(\d+)', self.get_url())
        if not re_id:
            raise AttributeError
        self.__temp['id'] = re_id.group(1)
        uri = '{}/detail/{}'.format(self.get_domain(), self.__temp['id'])
        self.__temp['content'] = self.http_get(uri)
        return self._check_source(self.__temp['content'])

    def get_manga_name(self):
        name = self.json.loads(self.__temp['content'])['name']
        return self.re.sub('[@$:/\\\]', '_', name)

    def get_chapters(self):
        uri = '{}/detail/{}?source={}'.format(
            self.get_domain(),
            self.__temp['id'],
            self.__temp['content']['source']
        )
        response = self.http_get(uri)
        try:
            items = self.json.loads(response)['chapters']
            items.reverse()
            return items
        except self.json.JSONDecodeError:
            return []

    def get_files(self):
        volume = self.get_current_chapter()
        if not self.__temp['id'] or 'cid' not in volume:
            return []
        uri = '{}/page/mangareader/{}/{}'.format(
            self.get_domain(),
            self.__temp['id'],
            volume['cid']
        )
        content = self.json.loads(self.http_get(uri))
        return [i['link'] for i in content['pages']]

    def get_cookies(self):
        pass

    def _loop_callback_volumes(self):
        pass

    def _loop_callback_files(self):
        pass


def provider():
    return Bulumanga
