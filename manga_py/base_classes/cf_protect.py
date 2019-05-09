from sys import stderr
import cloudscraper


class CloudFlareProtect:
    protector = []

    def run(self, url):  # pragma: no cover

        if not self.protector:
            scraper = cloudscraper.create_scraper()
            try:
                self.protector = scraper.get_tokens(url)
            except Exception as e:
                print('CF error! %s' % e, file=stderr)

        return self.protector
