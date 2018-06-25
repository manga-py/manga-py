from sys import stderr
import cfscrape


class CloudFlareProtect:
    protector = []

    def run(self, url):  # pragma: no cover

        if not self.protector:
            scr = cfscrape.create_scraper()
            try:
                self.protector = scr.get_tokens(url)
            except Exception as e:
                print('CF error! %s' % e, file=stderr)

        return self.protector
