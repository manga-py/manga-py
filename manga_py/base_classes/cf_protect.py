import cloudscraper
from logging import error


def cf_scrape(url):  # pragma: no cover

    scraper = cloudscraper.create_scraper()
    try:
        return scraper.get_tokens(url)
    except Exception as e:
        error(e)
        raise e
