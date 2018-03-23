from urllib.parse import urlparse

from manga_py.http.url_normalizer import normalize_uri
from manga_py.provider import Provider


class JavZipOrg:
    parser = None
    url = None
    domain = None

    def __init__(self, parser: Provider):
        self.parser = parser
        url = parser.chapter
        if parser.re.search(r'jav-zip\.org', url):
            self.url = url
            _ = urlparse(url)
            self.domain = _.scheme + '://' + _.netloc

    def _parse_id(self):
        return self.parser.re.search('/.p=(\d+)', self.url).group(1)

    def parse_images(self, content):
        images = []
        for i in content.cssselect('img'):
            src = normalize_uri(i.get('src'), self.url)
            images.append(src)
        return images

    def get(self, step):
        url = '{}/wp-admin/admin-ajax.php?post={}&action=get_content&step={}'
        url = url.format(self.domain, self._parse_id, step)
        content = self.parser.json.loads(self.parser.http_get(url))
        content = self.parser.document_fromstring(content['mes'])
        allow_more = True
        if len(content.cssselect('a.view-more')) < 1:
            allow_more = False
        return allow_more, content

    def get_images(self):
        if not self.url:
            return []
        images = []
        step = 0
        allow_more = True
        while allow_more:
            allow_more, content = self.get(step)
            step += 50  # constant
            images += self.parse_images(content)
        return images
