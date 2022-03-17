#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from manga_py import meta

RE_VALID_PACKAGE = re.compile(r'^([a-zA-Z-_]+)')
RE_REPLACE_SETUP_REQ = re.compile(r'^(REQUIREMENTS\s*=\s*\[)(.*\])$')


def req_lines():
    with open('requirements.txt', 'r') as _r:
        return [line.strip() for line in _r.readlines() if RE_VALID_PACKAGE.search(line)]


with open('manga_py/cli/_requirements.py', 'w') as w:
    w.write('requirements = ["%s"]' % '","'.join(req_lines()))


def req(lines: list):
    requirements = ''.join(["'%s', " % line for line in req_lines()])

    for n, line in enumerate(lines):
        matched = RE_REPLACE_SETUP_REQ.search(line)
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
