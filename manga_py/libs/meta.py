from manga_py.provider import Provider

# Describes the structure of the files, chapters


class File:
    idx = 0
    name = None
    provider = None

    def __init__(self, provider: Provider, idx: int, data):
        self.provider = provider
        self.idx = idx

    def normalize_name(self, name):
        if self.provider.arg('rename-pages'):
            return '{:0>3}'.format(self.idx)
        return '{:0>3}_{}'.format(self.idx, name)


class Chapter:
    idx = 0
    name = None
    provider = None

    def __init__(self, provider: Provider, idx: int, data):
        self.provider = provider
        self.idx = idx
