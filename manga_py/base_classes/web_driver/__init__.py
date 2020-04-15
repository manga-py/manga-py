from logging import info, error, debug

__all__ = ['display', 'get_driver']

display = None
driver = None


def get_driver(browser: str = None):
    global driver
    global display

    if driver is not None:
        return driver

    try:
        from selenium.webdriver import __version__
    except ImportError as e:
        error('Selenium not installed. Please, run "pip install selenium"')
        raise e

    display = _init_display()

    if browser is None:
        driver = _auto_browser()
    elif browser == 'chrome':
        driver = _chrome()
    elif browser == '_firefox':
        driver = _firefox()
    else:
        raise RuntimeError('Bad driver type')


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
        debug('Use chrome')
        return _driver
    except Exception as ce:
        try:
            _driver = _firefox()
            debug('Use _firefox')
            return _driver
        except Exception as e:
            error('Browser driver init error', ce, e)
            raise e


def _chrome():
    try:
        from .chrome import ChromeDriver
        return ChromeDriver().init_driver()
    except Exception as e:
        error('Chrome browser driver init error')
        raise e


def _firefox():
    try:
        from .firefox import FirefoxDriver
        return FirefoxDriver().init_driver()
    except Exception as e:
        error('Firefox browser driver init error')
        raise e
