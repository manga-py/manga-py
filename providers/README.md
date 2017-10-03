# All providers

### For template example, see _template.py

## Functions:

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from lxml.html import document_fromstring
# import re
# import json


def get_main_content(url: str, get: callable, post: callable):
    """
    :param url: str
    :param get: request.get
    :param post: request.post
    :return: mixed (1)
    """
    pass


def get_volumes(content=None, url: str, get: callable, post: callable):
    """
    :param content: mixed (1) (Content from get_main_content)
    :param url: str
    :param get: request.get
    :param post: request.post
    :return: array (2)
    """
    pass


def get_archive_name(volume, index: int = None) -> str:
    """
    :param volume: mixed (2) mixed element from get_volumes
    :param index: int
    :return: str
    """
    pass


def get_images(main_content=None, volume=None, get=None, post=None) -> list:
    """
    :param main_content: mixed (1)
    :param volume: mixed (2)
    :param get: request.get
    :param post: request.post
    :return: list
    """
    pass


def get_manga_name(url, get=callable):
    """
    :param url: str
    :param get: request.get
    :return: str
    """
    pass


# NOT REQUIRED /*

# if True, use zip_list(). get_images() alternative
download_zip_only = None


def get_zip(main_content=None, volume=None, get: callable, post: callable):
    """
    :param main_content: mixed (1) (Content from get_main_content)
    :param volume: mixed (2) (Mixed element from get_volumes)
    :param get: request.get
    :param post: request.post
    :return: str|list
    """
    pass

# if not None - additional cookies
# cookies = [
#  {
#    'value': 'cookie value',
#    'domain': 'asd.domain',
#    'path': '/cookie/path/',
#    'name': 'cookie_name',
#  },
#  'Browser'
# ]
cookies = None

# */ NOT REQUIRED

```