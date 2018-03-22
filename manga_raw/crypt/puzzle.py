from PIL import Image


class Puzzle:
    need_copy_orig = False

    __x = 0
    __y = 0
    __multiply = 1
    __matrix = None
    __image_src = None
    __image_dst = None
    __block_width = None
    __block_height = None

    def __init__(self, x: int, y: int, matrix: dict, multiply: int = 1):
        self.__x = x
        self.__y = y
        self.__matrix = matrix
        self.__multiply = multiply

    def de_scramble(self, path_src: str, path_dst: str):
        self.__image_src = Image.open(path_src, 'r')
        self._process()
        self.__image_dst.save(path_dst)
        self.__image_src.close()
        self.__image_dst.close()

    def _process(self):
        self.__image_dst = Image.new(self.__image_src.mode, self.__image_src.size)
        self._calc_block_size()
        self._check_copy_orig_image()
        self._solve_matrix()

    def _check_copy_orig_image(self):
        if self.need_copy_orig:
            self.__image_dst.paste(self.__image_src)

    def _calc_block_size(self):
        if self.__multiply <= 1:
            self.__block_width = int(self.__image_src.size[0] / self.__x)
            self.__block_height = int(self.__image_src.size[1] / self.__y)
        else:
            self.__block_width = self.__multiply * int(self.__image_src.size[0] / self.__y / self.__multiply)
            self.__block_height = self.__multiply * int(self.__image_src.size[1] / self.__x / self.__multiply)

    def _src_rect(self, i):
        row = int(i / self.__x)
        col = i - row * self.__x
        x = col * self.__block_width
        y = row * self.__block_height
        return x, y, x + self.__block_width, y + self.__block_height

    def _dst_rect(self, i):
        row = int(self.__matrix[i] / self.__x)
        col = self.__matrix[i] - row * self.__y
        x = col * self.__block_width
        y = row * self.__block_height
        return x, y, x + self.__block_width, y + self.__block_height

    def _solve_matrix(self):
        for i in range(self.__x * self.__y):
            src_rect = self._src_rect(i)
            dst_rect = self._dst_rect(i)
            region = self.__image_src.crop(src_rect)
            self.__image_dst.paste(region, dst_rect)
