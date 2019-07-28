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

see https://yuru-yuri.github.io/manga-py/#resources-list

Plans for improvement:
----------------------

see https://yuru-yuri.github.io/manga-py/improvement.html

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
See https://github.com/yuru-yuri/manga-py/issues/48

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


.. |Travis CI result| image:: https://travis-ci.org/yuru-yuri/manga-py.svg?branch=stable_1.x
   :target: https://travis-ci.org/yuru-yuri/manga-py/branches
.. |Code Climate| image:: https://codeclimate.com/github/yuru-yuri/manga-py/badges/gpa.svg
   :target: https://codeclimate.com/github/yuru-yuri/manga-py
.. |Issue Count| image:: https://codeclimate.com/github/yuru-yuri/manga-py/badges/issue_count.svg
   :target: https://codeclimate.com/github/yuru-yuri/manga-py
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/manga-py.svg
   :target: https://pypi.org/project/manga-py/
.. |Scrutinizer CI result| image:: https://scrutinizer-ci.com/g/yuru-yuri/manga-py/badges/quality-score.png?b=stable_1.x
   :target: https://scrutinizer-ci.com/g/yuru-yuri/manga-py
.. |Scrutinizer CI coverage| image:: https://scrutinizer-ci.com/g/yuru-yuri/manga-py/badges/coverage.png?b=stable_1.x
   :target: https://scrutinizer-ci.com/g/yuru-yuri/manga-py
.. |GitHub issues| image:: https://img.shields.io/github/issues/yuru-yuri/manga-py.svg
   :target: https://github.com/yuru-yuri/manga-py/issues
.. |PyPi version| image:: https://badge.fury.io/py/manga-py.svg
   :alt: PyPI
   :target: https://pypi.org/project/manga-py/
.. |JetBrains logo| image:: https://github.com/yuru-yuri/manga-py/raw/stable_1.x/.github/jetbrains.png
   :alt: JetBrains
   :target: https://www.jetbrains.com/?from=manga-py
