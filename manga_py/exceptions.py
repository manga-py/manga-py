class InvalidUrlException(RuntimeError):
    def __init__(self, url, *args, **kwargs):
        self._url = url
        super().__init__(*args, **kwargs)

    def url(self):
        return self._url


class NetworkException(RuntimeError):
    @classmethod
    def create(cls):
        return cls('Network error')


class InvalidFile(RuntimeError):
    pass


class ProviderNotFoundException(RuntimeError):
    @classmethod
    def create(cls, url: str):
        return cls('Provider not found for url ' + url)


class JsonException(RuntimeError):
    def __init__(self, content, *args, **kwargs):
        self._content = content
        super().__init__(*args, **kwargs)

    def content(self):
        return self._content


class FsError(RuntimeError):
    pass


class SpaceLeftException(RuntimeError):
    @classmethod
    def create(cls, path: str):
        cls('No space left on device (%s)' % str(path))


__all__ = [
    'InvalidUrlException', 'NetworkException', 'InvalidFile', 'ProviderNotFoundException',
    'JsonException', 'FsError', 'SpaceLeftException',
]
