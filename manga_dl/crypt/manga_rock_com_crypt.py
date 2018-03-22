from .base_lib import BaseLib


class MangaRockComCrypt(BaseLib):
    def decrypt(self, string):
        if isinstance(string, str):
            string = string.encode()
        n = len(string) + 7

        tmp = self.pack_auto([82, 73, 70, 70])

        tmp += self.pack_auto([
            n & 0xff,
            (n >> 8) & 0xff,
            (n >> 16) & 0xff,
            (n >> 24) & 0xff,
        ])

        tmp += self.pack_auto([87, 69, 66, 80, 86, 80, 56])
        for i in range(len(string)):
            tmp += self.pack('1B', string[i] ^ 101)
        return tmp
