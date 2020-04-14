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

    try:
        from pyvirtualdisplay import Display
        display = Display(visible=False, size=(1920, 1080))
        display.start()
    except ImportError:
        display = None
        info('Use real display. See here: https://github.com/ponty/PyVirtualDisplay/blob/master/README.rst')

    if browser is None:
        try:
            driver = _chrome()
            debug('Use chrome')
            return driver
        except Exception as ce:
            try:
                driver = _firefox()
                debug('Use _firefox')
                return driver
            except Exception as e:
                error('Browser driver init error', ce, e)
                raise e
    elif browser == 'chrome':
        try:
            return _chrome()
        except Exception as e:
            error('Browser driver init error')
            raise e
    elif browser == '_firefox':
        try:
            return _firefox()
        except Exception as e:
            error('Browser driver init error')
            raise e
    else:
        raise RuntimeError('Bad driver type')


def _chrome():
    from .chrome import ChromeDriver
    return ChromeDriver().init_driver()


def _firefox():
    from .firefox import FirefoxDriver
    return FirefoxDriver().init_driver()
