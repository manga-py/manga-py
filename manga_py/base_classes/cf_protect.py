import cloudscraper
from loguru import logger


def cf_scrape(url):  # pragma: no cover

    scraper = cloudscraper.create_scraper()
    try:
        return scraper.get_tokens(url)
    except Exception as e:
        logger.error(e)
        raise e
