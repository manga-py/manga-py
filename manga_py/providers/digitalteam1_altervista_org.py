from .read_powermanga_org import ReadPowerMangaOrg


class DigitalTeam1AltervistaOrg(ReadPowerMangaOrg):
    __title = None
    _name_re = '/reader/[^/]+/([^/]+)'
    _content_str = '{}/reader/read/{}/'
    _chapters_selector = '.chapter_list li > div > a'

    def get_chapters(self):
        self.__title = self.text_content(self.content, 'title')
        return super().get_chapters()

    def __parse_json(self, data) -> list:
        items = []
        for n, i in enumerate(data[0]):
            items.append('{}/reader{}{}{}{}'.format(
                self.domain,
                data[2],  # path
                i['name'],  # image index
                data[1][n],  # image hash
                i['ex']  # image extension
            ))
        return items

    def get_files(self):
        chapter = self.re.search('/(\d+)/', self.chapter).group(1)
        data = {
            'info[manga]': self.manga_name,
            'info[chapter]': chapter,
            'info[ch_sub]': '0',  # todo: watch this
            'info[title]': self.__title,
        }
        with self.http().post(
            '{}/reader/c_i'.format(self.domain),
            data=data,
            headers={'X-Requested-With': 'XMLHttpRequest'}
        ) as resp:
            json = resp.json()

        if isinstance(json, str):  # DO NOT TOUCH THIS!
            json = self.json.loads(json)

        return self.__parse_json(json)

    def get_cover(self) -> str:
        return self._cover_from_content('.cover img')


main = DigitalTeam1AltervistaOrg
