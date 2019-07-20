Manga-Downloader |Travis CI result|
===================================

Universal assistant download manga.
'''''''''''''''''''''''''''''''''''

Approximately 300 providers are available now.
''''''''''''''''''''''''''''''''''''''''''''''

|Code Climate| |Issue Count| |PyPI - Python Version|

|Scrutinizer CI result| |Scrutinizer CI coverage| |GitHub issues| |PyPi version|

Supported resources
-------------------

see https://yuru-yuri.github.io/manga-dl/#resources-list

Plans for improvement:
----------------------

see https://yuru-yuri.github.io/manga-dl/improvement.html

How to use
----------

Installation
~~~~~~~~~~~~

1) Download python 3.5+ https://www.anaconda.com/downloads
2) Install pip package:

   .. code:: bash

       pip install manga-py

3) Run program:

.. code:: bash

    manga-py http://manga.url/manga/name  # For download manga

Installation on the Android
~~~~~~~~~~~~~~~~~~~~~~~~~~~
See https://github.com/yuru-yuri/manga-dl/issues/48

Docker image:
~~~~~~~~~~~~~
https://hub.docker.com/r/mangadl/manga-py


Downloading manga
-----------------

**:warning:For sites with cloudflare protect need installed Node.js**

**:warning:Notice! By default, the mode of multithreaded image loading
is enabled**

**To change this behavior, add the key --no-multi-threads**

.. code:: bash

    # download to "./Manga/<manga-name-here>" directory
    manga-py http://manga-url-here/manga-name
    # download to "./Manga/Manga Name" directory
    manga-py http://manga-url-here/manga-name --name 'Manga Name'
    # or download to /manga/destination/path/<manga-name-here> directory
    manga-py http://manga-url-here/manga-name -d /manga/destination/path/
    # skip 3 volumes
    manga-py --skip-volumes 3 http://manga-url-here/manga-name
    # skip 3 volumes and download 2 volumes
    manga-py --skip-volumes 3 --max-volumes 2 http://manga-url-here/manga-name
    # reverse volumes downloading (24 -> 1)
    manga-py --reverse-downloading http://manga-url-here/manga-name
    # Disable progressbar
    manga-py --no-progress http://manga-url-here/manga-name

Help
----

.. code:: bash

    manga-py -h
    # or
    manga-py --help

Suported by JetBrains
---------------------
|JetBrains logo|


.. |Travis CI result| image:: https://travis-ci.org/yuru-yuri/manga-dl.svg?branch=stable_1.x
   :target: https://travis-ci.org/yuru-yuri/manga-dl/branches
.. |Code Climate| image:: https://codeclimate.com/github/yuru-yuri/manga-dl/badges/gpa.svg
   :target: https://codeclimate.com/github/yuru-yuri/manga-dl
.. |Issue Count| image:: https://codeclimate.com/github/yuru-yuri/manga-dl/badges/issue_count.svg
   :target: https://codeclimate.com/github/yuru-yuri/manga-dl
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/manga-py.svg
   :target: https://pypi.org/project/manga-py/
.. |Scrutinizer CI result| image:: https://scrutinizer-ci.com/g/yuru-yuri/manga-dl/badges/quality-score.png?b=stable_1.x
   :target: https://scrutinizer-ci.com/g/yuru-yuri/manga-dl
.. |Scrutinizer CI coverage| image:: https://scrutinizer-ci.com/g/yuru-yuri/manga-dl/badges/coverage.png?b=stable_1.x
   :target: https://scrutinizer-ci.com/g/yuru-yuri/manga-dl
.. |GitHub issues| image:: https://img.shields.io/github/issues/yuru-yuri/manga-dl.svg
   :target: https://github.com/yuru-yuri/manga-dl/issues
.. |PyPi version| image:: https://badge.fury.io/py/manga-py.svg
   :alt: PyPI
   :target: https://pypi.org/project/manga-py/
.. |JetBrains logo| image:: data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE5LjEuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPgo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4IgoJIHdpZHRoPSIxMjAuMXB4IiBoZWlnaHQ9IjEzMC4ycHgiIHZpZXdCb3g9IjAgMCAxMjAuMSAxMzAuMiIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgMTIwLjEgMTMwLjI7IiB4bWw6c3BhY2U9InByZXNlcnZlIgoJPgo8Zz4KCTxsaW5lYXJHcmFkaWVudCBpZD0iWE1MSURfMl8iIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIiB4MT0iMzEuODQxMiIgeTE9IjEyMC41NTc4IiB4Mj0iMTEwLjI0MDIiIHkyPSI3My4yNCI+CgkJPHN0b3AgIG9mZnNldD0iMCIgc3R5bGU9InN0b3AtY29sb3I6I0ZDRUUzOSIvPgoJCTxzdG9wICBvZmZzZXQ9IjEiIHN0eWxlPSJzdG9wLWNvbG9yOiNGMzdCM0QiLz4KCTwvbGluZWFyR3JhZGllbnQ+Cgk8cGF0aCBpZD0iWE1MSURfMzA0MV8iIHN0eWxlPSJmaWxsOnVybCgjWE1MSURfMl8pOyIgZD0iTTExOC42LDcxLjhjMC45LTAuOCwxLjQtMS45LDEuNS0zLjJjMC4xLTIuNi0xLjgtNC43LTQuNC00LjkKCQljLTEuMi0wLjEtMi40LDAuNC0zLjMsMS4xbDAsMGwtODMuOCw0NS45Yy0xLjksMC44LTMuNiwyLjItNC43LDQuMWMtMi45LDQuOC0xLjMsMTEsMy42LDEzLjljMy40LDIsNy41LDEuOCwxMC43LTAuMmwwLDBsMCwwCgkJYzAuMi0wLjIsMC41LTAuMywwLjctMC41bDc4LTU0LjhDMTE3LjMsNzIuOSwxMTguNCw3Mi4xLDExOC42LDcxLjhMMTE4LjYsNzEuOEwxMTguNiw3MS44eiIvPgoJPGxpbmVhckdyYWRpZW50IGlkPSJYTUxJRF8zXyIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiIHgxPSI0OC4zNjA3IiB5MT0iNi45MDgzIiB4Mj0iMTE5LjkxNzkiIHkyPSI2OS41NTQ2Ij4KCQk8c3RvcCAgb2Zmc2V0PSIwIiBzdHlsZT0ic3RvcC1jb2xvcjojRUY1QTZCIi8+CgkJPHN0b3AgIG9mZnNldD0iMC41NyIgc3R5bGU9InN0b3AtY29sb3I6I0YyNkY0RSIvPgoJCTxzdG9wICBvZmZzZXQ9IjEiIHN0eWxlPSJzdG9wLWNvbG9yOiNGMzdCM0QiLz4KCTwvbGluZWFyR3JhZGllbnQ+Cgk8cGF0aCBpZD0iWE1MSURfMzA0OV8iIHN0eWxlPSJmaWxsOnVybCgjWE1MSURfM18pOyIgZD0iTTExOC44LDY1LjFMMTE4LjgsNjUuMUw1NSwyLjVDNTMuNiwxLDUxLjYsMCw0OS4zLDAKCQljLTQuMywwLTcuNywzLjUtNy43LDcuN3YwYzAsMi4xLDAuOCwzLjksMi4xLDUuM2wwLDBsMCwwYzAuNCwwLjQsMC44LDAuNywxLjIsMWw2Ny40LDU3LjdsMCwwYzAuOCwwLjcsMS44LDEuMiwzLDEuMwoJCWMyLjYsMC4xLDQuNy0xLjgsNC45LTQuNEMxMjAuMiw2Ny4zLDExOS43LDY2LDExOC44LDY1LjF6Ii8+Cgk8bGluZWFyR3JhZGllbnQgaWQ9IlhNTElEXzRfIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjUyLjk0NjciIHkxPSI2My42NDA3IiB4Mj0iMTAuNTM3OSIgeTI9IjM3LjE1NjIiPgoJCTxzdG9wICBvZmZzZXQ9IjAiIHN0eWxlPSJzdG9wLWNvbG9yOiM3QzU5QTQiLz4KCQk8c3RvcCAgb2Zmc2V0PSIwLjM4NTIiIHN0eWxlPSJzdG9wLWNvbG9yOiNBRjRDOTIiLz4KCQk8c3RvcCAgb2Zmc2V0PSIwLjc2NTQiIHN0eWxlPSJzdG9wLWNvbG9yOiNEQzQxODMiLz4KCQk8c3RvcCAgb2Zmc2V0PSIwLjk1NyIgc3R5bGU9InN0b3AtY29sb3I6I0VEM0Q3RCIvPgoJPC9saW5lYXJHcmFkaWVudD4KCTxwYXRoIGlkPSJYTUxJRF8zMDQyXyIgc3R5bGU9ImZpbGw6dXJsKCNYTUxJRF80Xyk7IiBkPSJNNTcuMSw1OS41QzU3LDU5LjUsMTcuNywyOC41LDE2LjksMjhsMCwwbDAsMGMtMC42LTAuMy0xLjItMC42LTEuOC0wLjkKCQljLTUuOC0yLjItMTIuMiwwLjgtMTQuNCw2LjZjLTEuOSw1LjEsMC4yLDEwLjcsNC42LDEzLjRsMCwwbDAsMEM2LDQ3LjUsNi42LDQ3LjgsNy4zLDQ4YzAuNCwwLjIsNDUuNCwxOC44LDQ1LjQsMTguOGwwLDAKCQljMS44LDAuOCwzLjksMC4zLDUuMS0xLjJDNTkuMyw2My43LDU5LDYxLDU3LjEsNTkuNXoiLz4KCTxsaW5lYXJHcmFkaWVudCBpZD0iWE1MSURfNV8iIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIiB4MT0iNTIuMTczNiIgeTE9IjMuNzAxOSIgeDI9IjEwLjc3MDYiIHkyPSIzNy44OTcxIj4KCQk8c3RvcCAgb2Zmc2V0PSIwIiBzdHlsZT0ic3RvcC1jb2xvcjojRUY1QTZCIi8+CgkJPHN0b3AgIG9mZnNldD0iMC4zNjQiIHN0eWxlPSJzdG9wLWNvbG9yOiNFRTRFNzIiLz4KCQk8c3RvcCAgb2Zmc2V0PSIxIiBzdHlsZT0ic3RvcC1jb2xvcjojRUQzRDdEIi8+Cgk8L2xpbmVhckdyYWRpZW50PgoJPHBhdGggaWQ9IlhNTElEXzMwNTdfIiBzdHlsZT0iZmlsbDp1cmwoI1hNTElEXzVfKTsiIGQ9Ik00OS4zLDBjLTEuNywwLTMuMywwLjYtNC42LDEuNUw0LjksMjguM2MtMC4xLDAuMS0wLjIsMC4xLTAuMiwwLjJsLTAuMSwwCgkJbDAsMGMtMS43LDEuMi0zLjEsMy0zLjksNS4xQy0xLjUsMzkuNCwxLjUsNDUuOSw3LjMsNDhjMy42LDEuNCw3LjUsMC43LDEwLjQtMS40bDAsMGwwLDBjMC43LTAuNSwxLjMtMSwxLjgtMS42bDM0LjYtMzEuMmwwLDAKCQljMS44LTEuNCwzLTMuNiwzLTYuMXYwQzU3LjEsMy41LDUzLjYsMCw0OS4zLDB6Ii8+Cgk8ZyBpZD0iWE1MSURfMzAwOF8iPgoJCTxyZWN0IGlkPSJYTUxJRF8zMDMzXyIgeD0iMzQuNiIgeT0iMzcuNCIgc3R5bGU9ImZpbGw6IzAwMDAwMDsiIHdpZHRoPSI1MSIgaGVpZ2h0PSI1MSIvPgoJCTxyZWN0IGlkPSJYTUxJRF8zMDMyXyIgeD0iMzkiIHk9Ijc4LjgiIHN0eWxlPSJmaWxsOiNGRkZGRkY7IiB3aWR0aD0iMTkuMSIgaGVpZ2h0PSIzLjIiLz4KCQk8ZyBpZD0iWE1MSURfMzAwOV8iPgoJCQk8cGF0aCBpZD0iWE1MSURfMzAzMF8iIHN0eWxlPSJmaWxsOiNGRkZGRkY7IiBkPSJNMzguOCw1MC44bDEuNS0xLjRjMC40LDAuNSwwLjgsMC44LDEuMywwLjhjMC42LDAsMC45LTAuNCwwLjktMS4ybDAtNS4zbDIuMywwCgkJCQlsMCw1LjNjMCwxLTAuMywxLjgtMC44LDIuM2MtMC41LDAuNS0xLjMsMC44LTIuMywwLjhDNDAuMiw1Mi4yLDM5LjQsNTEuNiwzOC44LDUwLjh6Ii8+CgkJCTxwYXRoIGlkPSJYTUxJRF8zMDI4XyIgc3R5bGU9ImZpbGw6I0ZGRkZGRjsiIGQ9Ik00NS4zLDQzLjhsNi43LDB2MS45bC00LjQsMFY0N2w0LDBsMCwxLjhsLTQsMGwwLDEuM2w0LjUsMGwwLDJsLTYuNywwCgkJCQlMNDUuMyw0My44eiIvPgoJCQk8cGF0aCBpZD0iWE1MSURfMzAyNl8iIHN0eWxlPSJmaWxsOiNGRkZGRkY7IiBkPSJNNTUsNDUuOGwtMi41LDBsMC0ybDcuMywwbDAsMmwtMi41LDBsMCw2LjNsLTIuMywwTDU1LDQ1Ljh6Ii8+CgkJCTxwYXRoIGlkPSJYTUxJRF8zMDIyXyIgc3R5bGU9ImZpbGw6I0ZGRkZGRjsiIGQ9Ik0zOSw1NGw0LjMsMGMxLDAsMS44LDAuMywyLjMsMC43YzAuMywwLjMsMC41LDAuOCwwLjUsMS40djAKCQkJCWMwLDEtMC41LDEuNS0xLjMsMS45YzEsMC4zLDEuNiwwLjksMS42LDJ2MGMwLDEuNC0xLjIsMi4zLTMuMSwyLjNsLTQuMywwTDM5LDU0eiBNNDMuOCw1Ni42YzAtMC41LTAuNC0wLjctMS0wLjdsLTEuNSwwbDAsMS41CgkJCQlsMS40LDBDNDMuNCw1Ny4zLDQzLjgsNTcuMSw0My44LDU2LjZMNDMuOCw1Ni42eiBNNDMsNTlsLTEuOCwwbDAsMS41SDQzYzAuNywwLDEuMS0wLjMsMS4xLTAuOHYwQzQ0LjEsNTkuMiw0My43LDU5LDQzLDU5eiIvPgoJCQk8cGF0aCBpZD0iWE1MSURfMzAxOV8iIHN0eWxlPSJmaWxsOiNGRkZGRkY7IiBkPSJNNDYuOCw1NGwzLjksMGMxLjMsMCwyLjEsMC4zLDIuNywwLjljMC41LDAuNSwwLjcsMS4xLDAuNywxLjl2MAoJCQkJYzAsMS4zLTAuNywyLjEtMS43LDIuNmwyLDIuOWwtMi42LDBsLTEuNy0yLjVoLTFsMCwyLjVsLTIuMywwTDQ2LjgsNTR6IE01MC42LDU4YzAuOCwwLDEuMi0wLjQsMS4yLTF2MGMwLTAuNy0wLjUtMS0xLjItMQoJCQkJbC0xLjUsMHYySDUwLjZ6Ii8+CgkJCTxwYXRoIGlkPSJYTUxJRF8zMDE2XyIgc3R5bGU9ImZpbGw6I0ZGRkZGRjsiIGQ9Ik01Ni44LDU0bDIuMiwwbDMuNSw4LjRsLTIuNSwwbC0wLjYtMS41bC0zLjIsMGwtMC42LDEuNWwtMi40LDBMNTYuOCw1NHoKCQkJCSBNNTguOCw1OWwtMC45LTIuM0w1Nyw1OUw1OC44LDU5eiIvPgoJCQk8cGF0aCBpZD0iWE1MSURfMzAxNF8iIHN0eWxlPSJmaWxsOiNGRkZGRkY7IiBkPSJNNjIuOCw1NGwyLjMsMGwwLDguM2wtMi4zLDBMNjIuOCw1NHoiLz4KCQkJPHBhdGggaWQ9IlhNTElEXzMwMTJfIiBzdHlsZT0iZmlsbDojRkZGRkZGOyIgZD0iTTY1LjcsNTRsMi4xLDBsMy40LDQuNGwwLTQuNGwyLjMsMGwwLDguM2wtMiwwTDY4LDU3LjhsMCw0LjZsLTIuMywwTDY1LjcsNTR6IgoJCQkJLz4KCQkJPHBhdGggaWQ9IlhNTElEXzMwMTBfIiBzdHlsZT0iZmlsbDojRkZGRkZGOyIgZD0iTTczLjcsNjEuMWwxLjMtMS41YzAuOCwwLjcsMS43LDEsMi43LDFjMC42LDAsMS0wLjIsMS0wLjZ2MAoJCQkJYzAtMC40LTAuMy0wLjUtMS40LTAuOGMtMS44LTAuNC0zLjEtMC45LTMuMS0yLjZ2MGMwLTEuNSwxLjItMi43LDMuMi0yLjdjMS40LDAsMi41LDAuNCwzLjQsMS4xbC0xLjIsMS42CgkJCQljLTAuOC0wLjUtMS42LTAuOC0yLjMtMC44Yy0wLjYsMC0wLjgsMC4yLTAuOCwwLjV2MGMwLDAuNCwwLjMsMC41LDEuNCwwLjhjMS45LDAuNCwzLjEsMSwzLjEsMi42djBjMCwxLjctMS4zLDIuNy0zLjQsMi43CgkJCQlDNzYuMSw2Mi41LDc0LjcsNjIsNzMuNyw2MS4xeiIvPgoJCTwvZz4KCTwvZz4KPC9nPgo8L3N2Zz4K
   :alt: JetBrains
   :width: 100 px
   :target: https://www.jetbrains.com/?from=manga-py
