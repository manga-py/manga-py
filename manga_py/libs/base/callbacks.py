class Callbacks:

    def __init__(self):
        super().__init__()

    def before_chapter(self, chapter):
        pass

    def after_chapter(self, chapter):
        pass

    def before_download(self, file):
        """ Before each file """
        pass

    def after_download(self, file):
        """ After each file """
        pass
