
import cfscrape


class CloudFlareProtect:

    protector = []

    @staticmethod
    def __get_domain(url, cookies):

        for d in cookies.list_domains():
            domain = cfscrape.urlparse(url).netloc
            if d.startswith(".") and d in ("." + domain):
                return d

    def run(self, url):

        if not len(self.protector):
            scr = cfscrape.create_scraper()
            response, user_agent = scr.get_tokens(url)
            domain = self.__get_domain(url, scr.cookies)

            self.protector = [
                {
                    'value': response.get('__cfduid'),
                    'domain': domain,
                    'path': '/',
                    'name': '__cfduid',
                },
                {
                    'value': response.get('cf_clearance'),
                    'domain': domain,
                    'path': '/',
                    'name': 'cf_clearance',
                },
                user_agent
            ]

        return self.protector
