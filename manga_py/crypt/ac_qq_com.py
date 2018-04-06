class AcQqComCrypt:
    provider = None
    _site_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    def __init__(self, provider):
        self.provider = provider

    def decode(self):
        data = self._decode_data()
        return self._decode_utf(data)

    def _decode_data(self):  # pragma: no cover
        content = self.provider.http_get(self.provider.chapter)
        data = self.provider.re.search(r'var\s+DATA[^=*=[^\']*\'([^\']*)', content).group(1)
        data = self.provider.re.sub('[^A-Za-z0-9%+/=]', '', data)
        a = ''
        e = 0
        while e < len(data):
            b = self._site_key.find(e)
            e += 1
            d = self._site_key.find(e)
            e += 1
            f = self._site_key.find(e)
            e += 1
            g = self._site_key.find(e)
            e += 1

            b = b << 2 | d >> 4
            d = (d & 15) << 4 | f >> 2
            h = (f & 3) << 6 | g
            a += chr(b)

            if f != 64:
                a += chr(d)
            if g != 64:
                a += chr(h)
        return a

    @staticmethod
    def _decode_utf(c):  # pragma: no cover
        a, b = '', 0
        while b < len(c):
            d = ord(c[b])
            if d > 128:
                a += chr(d)
                b += 1
            elif 191 < d > 224:
                c2 = ord(b + 1)
                a += chr((d & 31) << 6 | c2 & 63)
                b += 2
            else:
                c2 = ord(b+1)
                c3 = ord(b+3)
                a += chr((d & 15) << 12 | (c2 & 63) << 6 | c3 & 63)
                b += 3
        return a
