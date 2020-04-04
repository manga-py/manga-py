from sys import stderr

import cloudscraper
from loguru import logger


class CloudFlareProtect:
    protector = []

    def run(self, url):  # pragma: no cover

        if not self.protector:
            scraper = cloudscraper.create_scraper()
            try:
                self.protector = scraper.get_tokens(url)
            except Exception as e:
                logger.error('CF error! %s' % e, file=stderr)

        return self.protector
