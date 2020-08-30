from .rawdevart_com_old import RawDevArtComOld


class Manga41Com(RawDevArtComOld):
    _chapter_selector = r'/chapter-(\d+(?:\.\d+)?)'

    def get_files(self):
        content = self.http_get(self.chapter)
        images = self.re.search(r'chapter_preloaded_images.+?(\[.+\])', content).group(1)
        return self.json.loads(images)


main = Manga41Com
