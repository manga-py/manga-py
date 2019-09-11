from .mangahub_io import MangaHubIo


class MangaReaderSite(MangaHubIo):
    __manga_id = None
    __graphql = 'https://api2.mangahub.io/graphql?query={}'

    def get_chapter_index(self) -> str:
        return self.chapter_for_json().replace('.', '-')

    def get_chapters(self):
        chapters = self.json.loads(self.http_get(self.__graphql.format(
            '{manga(x:mr01,slug:"%s"){chapters{id,number,title,slug,date}}}' % self.manga_name
        )))
        return chapters.get('data', {}).get('manga', {}).get('chapters', [])[::-1]

    def get_files(self):
        data = self.http_get(self.__graphql.format(
            '{chapter(x:mr01,slug:"%s",number:%d){pages}}' % (self.manga_name, self.chapter['number'])
        ))
        images = self.json.loads(data)
        pages = self.json.loads(images.get('data', {}).get('chapter', {}).get('pages', '{}'))
        return ['https://cdn.mangahub.io/file/imghub/%s' % pages[i] for i in pages]

    def chapter_for_json(self) -> str:
        return str(self.chapter['number'])


main = MangaReaderSite
