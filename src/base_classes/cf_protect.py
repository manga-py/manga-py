
import cfscrape


class CloudFlareProtect:

    protector = []

    def run(self, url):  # pragma: no cover

        if not self.protector:
            scr = cfscrape.create_scraper()
            self.protector = scr.get_tokens(url)

        return self.protector
