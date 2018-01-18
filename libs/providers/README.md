# All providers

### For template example, see _template.py

## Functions:

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from libs.providers.provider import Provider


class _Template(Provider):

    def get_archive_name(self) -> str:
        pass

    def get_chapter_index(self) -> str:
        pass

    def get_main_content(self):  # call once
        pass

    def get_manga_name(self) -> str:  # call once
        return ''

    def get_chapters(self):  # call once
        return []

    def prepare_cookies(self):  # if site with cookie protect
        pass

    def get_files(self):  # call ever volume loop
        return []

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = _Template

```