import re
from typing import List, Optional, Tuple
from PIL import Image
from sys import stderr


class VizComMatrix:
    @classmethod
    def get_image_meta(cls, path: str) -> Optional[List[int]]:
        pattern = None
        try:
            with open(path, 'rb') as r:
                # read one line. get pattern
                pattern = re.search(r'([\da-f]{2}(?::[\da-f]{2})+)', str(r.readline(1024))).group(1)
                pattern = [int('0x%s' % i, 16) for i in pattern.split(':')]
        except Exception as e:
            print('Error extract pattern. Path: %s' % path, file=stderr)
        return pattern

    @classmethod
    def solve_image(cls, path: str) -> Optional[Image.Image]:
        meta = cls.get_image_meta(path)
        if meta is None:
            return

        orig = Image.open(path)  # type: Image.Image
        new_size = (orig.size[0] - 90, orig.size[1] - 140)
        ref = Image.new(orig.mode, new_size)  # type: Image.Image
        ref.paste(orig)

        width, height = ref.size
        small_width = int(width / 10)
        small_height = int(height / 15)

        cls.paste(ref, orig, (
            0, small_height + 10,
            small_width, height - 2 * small_height,
        ), (
            0, small_height,
            small_width, height - 2 * small_height,
        ))

        cls.paste(ref, orig, (
            0, 14 * (small_height + 10),
            width, orig.height - 14 * (small_height + 10),
        ), (
            0, 14 * small_height,
            width, orig.height - 14 * (small_height + 10),
        ))

        cls.paste(ref, orig, (
            9 * (small_width + 10), small_height + 10,
            small_width + (width - 10 * small_width), height - 2 * small_height,
        ), (
            9 * small_width, small_height,
            small_width + (width - 10 * small_width), height - 2 * small_height,
        ))

        for i, j in enumerate(cls.get_image_meta(path)):
            cls.paste(ref, orig, (
                (i % 8 + 1) * (small_width + 10), (int(i / 8) + 1) * (small_height + 10),
                small_width, small_height,
            ), (
                (j % 8 + 1) * small_width, (int(j / 8) + 1) * small_height,
                small_width, small_height,
            ))

        return ref

    @classmethod
    def paste(cls, ref: Image.Image, orig: Image.Image, orig_box: Tuple, ref_box: Tuple):
        ref.paste(orig.crop((
            int(orig_box[0]), int(orig_box[1]),
            int(orig_box[0] + orig_box[2]), int(orig_box[1] + orig_box[3]),
        )), (
            int(ref_box[0]), int(ref_box[1]),
            int(ref_box[0] + ref_box[2]), int(ref_box[1] + ref_box[3]),
        ))


solve = VizComMatrix().solve_image

__all__ = ['solve']
