try:
    from progressbar import ProgressBar
    from zenlog import Log
    from getpass import getpass
    from manga_py.libs.modules.info import Info
except ImportError:
    pass


class Methods:
    __methods = None
    _args = None

    def __init__(self):
        super().__init__()
        self.__methods = {}

    def __get_callback(self, key, default=None):
        func = self.__methods.get(key, None)
        if func is None:
            return lambda *args, **kwargs: default
        return func

    @property
    def logger(self):
        """
        Returned logger class with next methods:
        .debug('text')
        .info('text')
        .warn('text')
        .error('text')
        .critical('text')

        See https://github.com/manufacturaind/python-zenlog/

        :return:
        :rtype: Log
        """
        return self.__get_callback('logger')

    @logger.setter
    def logger(self, value):
        self.__methods['logger'] = value

    @property
    def print(self):
        __doc__ = print.__doc__
        return self.__get_callback('print')

    @print.setter
    def print(self, value):
        self.__methods['print'] = value

    @property
    def print_error(self):
        __doc__ = print.__doc__
        return self.__get_callback('print_error')

    @property
    def print_info(self):
        __doc__ = print.__doc__
        return self.__get_callback('print_error')

    @print_error.setter
    def print_error(self, value):
        self.__methods['print_error'] = value

    @property
    def input(self):
        __doc__ = input.__doc__
        return self.__get_callback('input')

    @input.setter
    def input(self, value):
        self.__methods['input'] = value

    @property
    def password(self):
        __doc__ = getpass.__doc__
        return self.__get_callback('password')

    @password.setter
    def password(self, value):
        self.__methods['password'] = value

    @property
    def info(self):
        """
        :return:
        :rtype: Info
        """
        return self.__get_callback('info')

    @info.setter
    def info(self, value):
        self.__methods['info'] = value

    @property
    def progressbar(self):
        """
        :return:
        :rtype: ProgressBar
        """
        return self.__get_callback('progressbar')

    @progressbar.setter
    def progressbar(self, value):
        self.__methods['progressbar'] = value

    def arg(self, key, default=None):
        key = key.replace('-', '_')
        return self._args.get(key, default)

    def _log(self) -> bool:
        return self.arg('show-log', False)

    def _verbose_log(self):
        return self.arg('verbose-log', False)

    def log_info(self, *args):
        self._verbose_log() and self.logger.info(*args)

    def log_warning(self, *args):
        self._log() and self.logger.warn(*args)

    def log_critical(self, *args):
        self.logger.critical(*args)
