from PIL import Image


# DO NOT SEE HERE! IT WORKED!


class MatrixSunday:
    __image_src = None
    __image_dst = None

    def de_scramble(self, path_src: str, path_dst: str, data: list):
        self.__image_src = Image.open(path_src, 'r')
        self.__process(data)
        self.__image_dst.save(path_dst)
        self.__image_src.close()
        self.__image_dst.close()

    def __process(self, data: list):
        size_src = self.__image_src.size

        self.__image_dst = Image.new(self.__image_src.mode, size_src)

        for i in data:
            x, y = i['srcX'] + i['width'], i['srcY'] + i['height']
            dx, dy = i['destX'] + i['width'], i['destY'] + i['height']

            c1 = i['srcX'] < size_src[0]
            c2 = i['srcX'] + i['width'] >= 0
            c3 = i['srcY'] < size_src[1]
            c4 = i['srcY'] + i['height'] >= 0
            if c1 and c2 and c3 and c4:
                region = self.__image_src.crop((i['destX'], i['destY'], dx, dy))
                self.__image_dst.paste(region, (i['srcX'], i['srcY'], x, y))


class SundayWebryCom:  # pragma: no cover
    _result = None

    def solve_by_img(self, src: str, element_width: int, element_height: int, n: int):
        img = Image.open(src)
        sizes = img.size
        img.close()
        return self.solve(*sizes, element_width, element_height, n)

    def solve(self, width: int, height: int, element_width: int, element_height: int, n: int):
        e = width
        t = height
        r = element_width
        i = element_height

        y = int(e / r)
        g = int(t / i)
        f = e % r
        b = t % i
        self._result = []

        s = y - 43 * n % y
        if s % y == 0:
            s = (y - 4) % y

        a = g - 47 * n % g
        if a % g == 0:
            a = (g - 4) % g
        if 0 == a:
            a = g - 1

        self.def1(f, b, s, r, a, i)

        self.def2(y, i, n, a, s, f, r, g, b)

        if f > 0:
            self.def3(g, n, s, a, y, b, i, r, f)

        self.def4(y, g, n, r, f, s, a, i, b)

        return self._result

    def def1(self, f, b, s, r, a, i):
        if f > 0 and b > 0:
            o = s * r
            u = a * i
            self._result.append({
                'srcX': o,
                'srcY': u,
                'destX': o,
                'destY': u,
                'width': f,
                'height': b,
                # 'debug': 1
            })

    def def2(self, y, i, n, a, s, f, r, g, b):
        for l in range(y):
            d = self._calc_x_x(l, y, n)
            h = self._calc_y_x(d, s, a, g, n)
            c = self._calc_pos_rest(d, s, f, r)
            p = h * i
            o = self._calc_pos_rest(l, s, f, r)
            u = a * i
            self._result.append({
                'srcX': o,
                'srcY': u,
                'destX': c,
                'destY': p,
                'width': r,
                'height': b,
                # 'debug': 2
            })

    def def3(self, g, n, s, a, y, b, i, r, f):
        for m in range(g):
            h = self._calc_y_y(m, g, n)
            d = self._calc_x_y(h, s, a, y, n)
            p = self._calc_pos_rest(h, a, b, i)
            u = self._calc_pos_rest(m, a, b, i)
            self._result.append({
                'srcX': s * r,
                'srcY': u,
                'destX': d * r,
                'destY': p,
                'width': f,
                'height': i,
                # 'debug': 3
            })

    def def4(self, y, g, n, r, f, s, a, i, b):
        for l in range(y):
            for m in range(g):
                d = (l + 29 * n + 31 * m) % y
                h = (m + 37 * n + 41 * d) % g
                c = d * r + (f if d >= self._calc_x_y(h, s, a, y, n) else 0)
                p = h * i + (b if h >= self._calc_y_x(d, s, a, g, n) else 0)
                o = l * r + (f if l >= s else 0)
                u = m * i + (b if m >= a else 0)
                self._result.append({
                    'srcX': o,
                    'srcY': u,
                    'destX': c,
                    'destY': p,
                    'width': r,
                    'height': i,
                    # 'debug': 4
                })

    @staticmethod
    def _calc_pos_rest(e, t, r, i):
        m = 0
        if e >= t:
            m = r
        return e * i + m

    @staticmethod
    def _calc_x_x(e, t, r):
        return (e + 61 * r) % t

    @staticmethod
    def _calc_x_y(e, t, r, i, n):
        o = (n % 2 == 1)
        if (e < r and o) or (e >= r and not o):
            a = i - t
            s = t
        else:
            a = t
            s = 0
        return (e + 67 * n + t + 71) % a + s

    @staticmethod
    def _calc_y_x(e, t, r, i, n):
        o = (n % 2 == 1)
        if (e < t and o) or (e >= t and not o):
            a = r
            s = 0
        else:
            a = i - r
            s = r
        return (e + 53 * n + 59 * r) % a + s

    @staticmethod
    def _calc_y_y(e, t, r):
        return (e + 73 * r) % t
