from .base_lib import BaseLib


class HentaiNexusComCrypt(BaseLib):
    def __init__(self):
        super().__init__()
        self._this = []
        self._pads = {}

    def decode(self, enc):
        buff = self.base64decode(enc)

        i = 0
        file = 0
        key = 0
        _hash = 0
        _input = []

        self._step_0()
        c = self._step_1(buff)
        index = self._step_3(buff, self._step_2())

        _next = self._this[c]

        for offset in range(64, len(buff)):
            i = (i + _next) % 256
            key = (file + index[(key + index[i]) % 256]) % 256
            file = (file + i + index[i]) % 256

            index[i], index[key] = index[key], index[i]

            _hash = index[(key + index[(i + index[(_hash + file) % 256]) % 256]) % 256]

            _input.append(chr(buff[offset] ^ _hash))

        return ''.join(_input)

    def _step_0(self):
        index = 2
        while len(self._this) < 16:
            try:
                _ = self._pads[index]
            except KeyError:
                self._this.append(index)
                week_index = index << 1

                while week_index <= 256:
                    self._pads[week_index] = True

                    week_index = week_index + index

            index += 1

    def _step_1(self, buff) -> int:
        c = 0

        for index in range(0, 64):
            c = c ^ buff[index]

            for week_index in range(0, 8):
                c = c >> 1 ^ 12 if c & 1 else c >> 1

        return c & 7

    def _step_2(self) -> list:
        return list(range(0, 256))

    def _step_3(self, buff, index: list) -> list:
        key = 0
        for i in range(0, 256):
            key = (key + index[i] + buff[i % 64]) % 256
            index[i], index[key] = index[key], index[i]

        return index


