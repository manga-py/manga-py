#!/usr/bin/python3
# -*- coding: utf-8 -*-

import manga
import providers.__for_make__

arguments = manga._arguments_parser().parse_args()
add_name = not arguments.no_name
name = arguments.name

if arguments.url:
    url = arguments.url
else:
    url = manga.manual_input('Please, paste manga url.')
    if add_name and len(name) < 1:
        name = manga.manual_input('Please, paste manga name')

setattr(manga, 'arguments', arguments)
setattr(manga, 'add_name', add_name)
manga.main(url, name)
