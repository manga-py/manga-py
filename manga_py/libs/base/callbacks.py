
class Callbacks:
    def before_chapter(self):
        pass

    def after_chapter(self):
        pass

    def before_download(self, url: str, idx: int) -> str:  # return url!
        return url

    def after_download(self, path, idx: int) -> str:  # return path!
        return path
