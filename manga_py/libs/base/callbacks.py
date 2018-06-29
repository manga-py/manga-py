
class Callbacks:
    def before_chapter(self):
        pass

    def after_chapter(self):
        pass

    def before_file_save(self, url: str, idx: int) -> str:  # return url!
        return url

    def after_file_save(self, _path, idx: int):
        pass
