
class Config:
    """
    :property image
    :property path
    :property download
    :property http
    """
    __params = None

    def __init__(self):
        self.__params = {}

    def __dir__(self):
        return self.__params.keys()

    def __setattr__(self, key: str, value):
        self.__params[key] = value

    def __getattribute__(self, key: str, default=None):
        return self.__params.get(key, default)

    def __delattr__(self, key):
        del self.__params[key]

    def import_args(self, args: dict):
        self.__params.update(args)
