try:
    from manga_py.provider import Provider
except ImportError:
    pass


class Api:
    """
    :type _provider Provider
    """
    _provider = None

    def __init__(self, provider):
        self._provider = provider
