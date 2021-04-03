import re
from typing import Optional, Tuple
from PIL import Image


WIDTH = 256
HEIGHT = 257
KEY = 42016

RE = re.compile(b'.+?([a-f0-9]{2}(?::[a-f0-9]{2})+)')


class VizComMatrix:
    @classmethod
    def solve_image(cls, path: str, metadata: dict) -> Optional[Image.Image]:
        orig = Image.open(path)  # type: Image.Image
        new_size = (orig.size[0] - 90, orig.size[1] - 140)
        ref = Image.new(orig.mode, new_size)  # type: Image.Image
        ref.paste(orig)

        exif = orig.getexif()

        if KEY in exif:
            key = [int(i, 16) for i in exif[KEY].split(':')]
            width, height = exif[WIDTH], exif[HEIGHT]
        else:
            exif_ = RE.search(orig.info.get('exif'))
            if exif_ is not None:
                key = [int(i, 16) for i in exif_.group(1).decode().split(':')]
                width, height = exif[WIDTH], exif[HEIGHT]
            else:
                key = []
                width, height = metadata['width'], metadata['height']

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

        for i, j in enumerate(key):
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
