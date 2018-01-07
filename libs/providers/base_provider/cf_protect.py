
import cfscrape
import tldextract


class CloudFlareProtect:

    cookies = []

    @staticmethod
    def _get_domain(url):
        ext = tldextract.extract(url)
        return '.%s.%s' % (ext.domain, ext.suffix)

    def run(self, url):

        if not len(self.cookies):
            domain = self._get_domain(url)
            scraper = cfscrape.get_tokens(url)
            if scraper is not None:
                self.cookies = []
                for i in scraper[0]:
                    self.cookies.append({
                        'value': scraper[0][i],
                        'domain': domain,
                        'path': '/',
                        'name': i,
                    })
                self.cookies.append(scraper[1])

        return self.cookies
