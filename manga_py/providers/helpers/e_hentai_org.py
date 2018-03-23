from manga_py.provider import Provider


class EHentaiOrg:
    provider = None

    def __init__(self, provider: Provider):
        self.provider = provider

    def get_pages_count(self, parser):
        selector = '.gtb table.ptt td[onclick] > a'
        paginate = parser.cssselect(selector)
        max_idx = 0
        for i in paginate:
            idx = self.provider.re.search(r'\?p=(\d+)', i.get('href'))
            max_idx = max(max_idx, int(idx.group(1)))
        return max_idx

    def get_image(self, i):
        url = i.get('href')
        src = self.provider.html_fromstring(url, 'img#img', 0)
        return src.get('src')

    def get_url(self):
        url = self.provider.get_url()
        if ~url.find('?'):
            url = url[:url.find('?')]
        if ~url.find('#'):
            url = url[:url.find('#')]
        return url
