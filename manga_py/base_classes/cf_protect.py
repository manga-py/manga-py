try:
    import cloudscraper as cfscrape
except ModuleNotFoundError:
    import cfscrape

# from logging import error
from pathlib import Path
from urllib.parse import urlparse, ParseResult
import json
from typing import Optional, Tuple
from ..fs import get_util_home_path
from time import time


CF_TIMEOUT = 3600 * 24 * 7  # 7 days


def cf_scrape(url):  # pragma: no cover
    cf = cf_load(url)

    if cf is not None:
        return cf

    scraper = cfscrape.create_scraper()
    try:
        cookies, ua = scraper.get_tokens(url)

        cf_save(url, cookies, ua)

        return cookies, ua
    except Exception as e:
        raise RuntimeError('cloudflare module not supported')
        # error(e)
        # raise e


def __domain(url: str) -> str:
    parsed = urlparse(url, 'https')  # type: ParseResult
    return parsed.hostname


def __cookies_location(url: str) -> Path:
    domain = __domain(url)
    path = get_util_home_path()
    return Path(path).joinpath('cf_cookies', '{}.dat'.format(domain))


def cf_save(url, cookies, ua):
    path = __cookies_location(url)
    path.parent.mkdir(exist_ok=True, parents=True)

    path.write_text(json.dumps({
        'cookies': cookies,
        'ua': ua,
        'time': int(time()),
    }))


def cf_load(url) -> Optional[Tuple[dict, str, int]]:
    try:
        path = __cookies_location(url)
        data = json.loads(path.read_text())

        if time() - data['time'] > CF_TIMEOUT:
            return None

        return data['cookies'], data['ua'], data['time']
    except (FileNotFoundError, NameError, ValueError, TypeError):
        return None
