class AcQqComCrypt:
    _provider = None
    _site_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    def __init__(self, provider):
        self._provider = provider

    def decode(self, data):
        data = self._provider.re.sub('[^A-Za-z0-9%+/=]', '', data)
        a = ''
        e = 0
        while e < len(data) - 4:
            e += 1
            b = self._site_key.find(data[e])
            e += 1
            d = self._site_key.find(data[e])
            e += 1
            f = self._site_key.find(data[e])
            e += 1
            g = self._site_key.find(data[e])

            b = b << 2 | d >> 4
            d = (d & 15) << 4 | f >> 2
            h = (f & 3) << 6 | g
            a += chr(b)

            if f != 64:
                a += chr(d)
            if g != 64:
                a += chr(h)
        return self._protect(a)

    def _protect(self, data):
        try:
            data = self._provider.re.search('({.+}})', data).group(1)
            return self._provider.json.loads(data)
        except Exception:
            return {}
