#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from manga_py import meta

RE = re.compile(r'^(REQUIREMENTS\s*=\s*\[)(.*\])$')


def req(lines: list):
    with open('requirements.txt', 'r') as _r:
        requirements = ''.join(["'%s', " % line.strip() for line in _r.readlines()])

    for n, line in enumerate(lines):
        matched = RE.search(line)
        if matched is not None:
            _b, _a = matched.groups()
            lines[n] = '%s%s%s' % (_b, requirements, _a)
            break

    return lines


with open('setup.py.template', 'r') as r:
    content = r.read()

    for key in meta.__all__:
        content = content.replace('__%s__' % key, getattr(meta, key))

    with open('setup.py', 'w') as w:
        w.write('\n'.join(req(content.splitlines())))
