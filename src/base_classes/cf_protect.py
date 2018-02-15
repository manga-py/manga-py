
import cfscrape


class CloudFlareProtect:

    protector = []

    def run(self, url):  # pragma: no cover

        if not self.protector:
            scr = cfscrape.create_scraper()
            try:
                self.protector = scr.get_tokens(url)
            except Exception:
                pass

        return self.protector
