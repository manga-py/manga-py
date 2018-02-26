#!/usr/bin/python3
# -*- coding: utf-8 -*-

import manga
import src.providers.__for_make__
import sys
from src.fs import is_dir, rmtree, get_temp_path
import atexit


@atexit.register
def before_shutdown():
    temp_dir = get_temp_path()
    is_dir(temp_dir) and rmtree(temp_dir)
    try:
        rmtree(sys._MEIPASS)
    except Exception:
        pass


manga.main()
