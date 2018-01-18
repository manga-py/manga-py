#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import providers

    content = ''

    for i in providers.providers_list:
        content = content + 'import libs.roviders.' + i + '\n'

    with open('libs/providers/__for_make__.py', 'w') as f:
        f.write(content)
        f.close()
