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
        """
        return self.__get_callback('logger')

    @logger.setter
    def logger(self, value):
        self.__methods['logger'] = value

    @property
    def print(self):
        return self.__get_callback('print')

    @print.setter
    def print(self, value):
        self.__methods['print'] = value

    @property
    def print_error(self):
        return self.__get_callback('print_error')

    @print_error.setter
    def print_error(self, value):
        self.__methods['print_error'] = value

    @property
    def input(self):
        return self.__get_callback('input')

    @input.setter
    def input(self, value):
        self.__methods['input'] = value

    @property
    def password(self):
        return self.__get_callback('password')

    @password.setter
    def password(self, value):
        self.__methods['password'] = value
        pass

    @property
    def info(self):
        return self.__get_callback('info')

    @info.setter
    def info(self, value):
        self.__methods['info'] = value

    @property
    def progressbar(self):
        return self.__get_callback('progressbar')

    @progressbar.setter
    def progressbar(self, value):
        self.__methods['progressbar'] = value

    def arg(self, key, default=None):
        return self._args.get(key, default)

    def _log(self):
        return self.arg('show_log', False)

    def _verbose_log(self):
        return self.arg('verbose_log', False)

    def log_info(self, *args):
        self._log() and self.logger.info(*args)

    def log_warning(self, *args):
        self._log() and self.logger.warn(*args)

    def log_crit(self, *args):
        self._log() and self.logger.critical(*args)
