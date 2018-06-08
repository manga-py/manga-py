# cli chapters parser
class ChapterHelper:
    chapters = ''

    def __init__(self, chapters: str):
        self.chapters = chapters
        if isinstance(self.chapters, str):
            self.chapters = self.chapters.split(' ')

    def get_chapters(self, urls):
        chapters = []
        for i, url in enumerate(urls):
            if i in self.chapters:
                chapters.append(urls)
        return chapters
