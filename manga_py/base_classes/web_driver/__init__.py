from logging import info, error

__all__ = ['get_display', 'make_driver']

__cache = {
    'display': None,
    'driver': None,
}


def get_display():
    return __cache['display']


def get_driver():
    return __cache['driver']


def make_driver(browser: str = None):
    if __cache['driver'] is not None:
        return __cache['driver']

    _assert_selenium()

    __cache['display'] = _init_display()

    if browser is None:
        __cache['driver'] = _auto_browser()
        return __cache['driver']

    if browser == 'chrome':
        __cache['driver'] = _chrome(True)
        return __cache['driver']

    if browser == 'firefox':
        __cache['driver'] = _firefox(True)
        return __cache['driver']

    raise RuntimeError('Bad driver type')


def _assert_selenium():
    try:
        from selenium.webdriver import __version__
    except ImportError as e:
        error('Selenium not installed. Please, run "pip install selenium"')
        raise e


def _init_display():
    try:
        from pyvirtualdisplay import Display
        _display = Display(visible=False, size=(1920, 1080))
        _display.start()
    except ImportError:
        _display = None
        info('Use real display. See here: https://github.com/ponty/PyVirtualDisplay/blob/master/README.rst')
    return _display


def _auto_browser():
    try:
        _driver = _chrome()
        info('Use chrome')
        return _driver
    except Exception as ce:
        try:
            _driver = _firefox()
            info('Use _firefox')
            return _driver
        except Exception as e:
            error('Browser driver init error', ce, e)
            raise e


def _chrome(show_error: bool = False):
    try:
        from .chrome import ChromeDriver
        return ChromeDriver().init_driver()
    except Exception as e:
        show_error and error('Chrome browser driver init error', e)
        raise e


def _firefox(show_error: bool = False):
    try:
        from .firefox import FirefoxDriver
        return FirefoxDriver().init_driver()
    except Exception as e:
        show_error and error('Firefox browser driver init error', e)
        raise e
