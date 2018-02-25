import requests
from lxml.html import document_fromstring


class AutoProxy:
    checked_url = 'https://httpbin.org/ip'

    @staticmethod
    def _s(item):
        s = lambda n: n.text_content().strip()
        td = item.cssselect('td')
        if s(td[4]) == 'anonymous' and s(td[6]) == 'yes':
            return s(td[0]) + ':' + s(td[1])
        return None

    def _test_proxy(self, url):
        proxies = {
            'http': url,
            'https': url,
        }
        try:
            requests.head(url=self.checked_url, proxies=proxies)
        except Exception:
            return False
        return proxies

    def _change_checked_url(self, checked_url):
        if checked_url:
            self.checked_url = checked_url

    def auto_proxy(self, checked_url=None):
        self._change_checked_url(checked_url)
        url = 'https://www.us-proxy.org'
        items = document_fromstring(requests.get(url).text).cssselect('#proxylisttable tbody tr')
        for i in items:
            proxy = self._s(i)
            test = False
            if proxy:
                test = self._test_proxy(proxy)
            if test:
                return test
        return None


auto_proxy = AutoProxy().auto_proxy
