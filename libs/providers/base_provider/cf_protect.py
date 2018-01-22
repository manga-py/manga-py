
import cfscrape


class CloudFlareProtect:

    protector = []

    def run(self, url):

        if not len(self.protector):
            scr = cfscrape.create_scraper()
            response, user_agent = scr.get_tokens(url)

            self.protector = [
                {
                    '__cfduid': response.get('__cfduid'),
                    'cf_clearance': response.get('cf_clearance'),
                },
                user_agent
            ]

        return self.protector
