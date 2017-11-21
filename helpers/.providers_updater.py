#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import providers

    content = """#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

    for i in providers.providers_list:
        content = content + 'import providers.' + i + '\n'

    with open('providers/__for_make__.py', 'w') as f:
        f.write(content)
