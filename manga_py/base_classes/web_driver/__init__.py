from logging import info, error, debug

__all__ = ['display', 'get_driver']

display = None
driver = None


def get_driver(browser: str = None):
    global driver
    if driver is not None:
        return driver

    try:
        from selenium.webdriver import __version__
    except ImportError:
        error('Selenium not installed. Please, run "pip install selenium"')
        exit()

    try:
        from pyvirtualdisplay import Display
        global display
        display = Display(visible=False, size=(1920, 1080))
        display.start()
    except ImportError:
        info('Use real display. See here: https://github.com/ponty/PyVirtualDisplay/blob/master/README.rst')

    if browser is None:
        try:
            driver = chrome()
            debug('Use chrome')
            return driver
        except Exception:
            try:
                driver = firefox()
                debug('Use firefox')
                return driver
            except Exception:
                error('Browser driver init error')
                exit(1)
    elif browser == 'chrome':
        try:
            return chrome()
        except Exception:
            error('Browser driver init error')
            exit(1)
    elif browser == 'firefox':
        try:
            return firefox()
        except Exception:
            error('Browser driver init error')
            exit(1)
    else:
        error('Bad driver type')
        exit(1)


def chrome():
    from .chrome import ChromeDriver
    driver = ChromeDriver()
    driver.init_driver()
    return driver


def firefox():
    from .firefox import FirefoxDriver
    driver = FirefoxDriver()
    driver.init_driver()
    return driver
