#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    from src.providers import providers_list

    content = ''

    for i in providers_list.keys():
        content = content + 'import src.providers.' + i + '\n'

    with open('src/providers/__for_make__.py', 'w') as f:
        f.write(content)
