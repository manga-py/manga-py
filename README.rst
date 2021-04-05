Manga-py |Travis CI result stable1.x|
==========================================

Universal assistant download manga.
'''''''''''''''''''''''''''''''''''

Approximately 200+ providers are available now.
'''''''''''''''''''''''''''''''''''''''''''''''

|Scrutinizer CI result| |Scrutinizer CI coverage| |GitHub issues| |Travis CI result|

|Code Climate| |Issue Count|

|GitHub repo size| |PyPI - size|

|PyPI - Python Version| |PyPi version| |PyPI - Downloads|

Supported resources
-------------------

see:

- https://manga-py.com/manga-py/#resources-list
- https://manga-py.github.io/manga-py/#resources-list (alternative)
- https://yuru-yuri.github.io/manga-py/#resources-list (deprecated)


Thanks for support
~~~~~~~~~~~~~~~~~~
1. Robert M.


How to use
----------

Installation
~~~~~~~~~~~~

1) Download python 3.6+ https://docs.conda.io/en/latest/miniconda.html
2) Install pip package:

.. code:: bash

   pip install manga-py

3) Run program:

.. code:: bash

    manga-py http://manga.url/manga/name  # For download manga

Installation on the Android
~~~~~~~~~~~~~~~~~~~~~~~~~~~
See https://github.com/manga-py/manga-py/issues/48

Docker image:
~~~~~~~~~~~~~
See:

- https://hub.docker.com/r/mangadl/manga-py/tags?page=1&ordering=last_updated


Downloading manga
-----------------

**:warning: For sites with cloudflare protect need installed Node.js**

**:warning: Notice! By default, the mode of multithreaded image loading is enabled**

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


Embedded example:
-----------------
https://github.com/manga-py/manga-py/blob/stable_1.x/embedded.md

Help
----

.. code:: bash

    manga-py -h
    # or
    manga-py --help

Suported by JetBrains
---------------------
|JetBrains logo|


Manga-py Docker
---------------

1. Install docker

  - Summary https://docs.docker.com/install/
  - Mac https://docs.docker.com/docker-for-mac/install/
  - Windows https://docs.docker.com/docker-for-windows/install/


2. Install manga-py

.. code:: bash

    docker pull mangadl/manga-py


3. Run it

.. code:: bash

    docker run -it -v ${PWD}:/home/manga mangadl/manga-py


For `manga-py >= 1.18`, the transfer of login / password / language / translation group has been added:

.. code:: bash

    manga-py http://... --arguments language=en login=my-login "password=secured-#\!Password" "translator=Awesome group"


.. |Travis CI result stable1.x| image:: https://travis-ci.com/manga-py/manga-py.svg?branch=stable_1.x
   :target: https://travis-ci.com/manga-py/manga-py/branches
   :alt: Latest push
.. |Travis CI result| image:: https://travis-ci.com/manga-py/manga-py.svg?branch=1.29.5
   :target: https://travis-ci.com/manga-py/manga-py/branches
   :alt: Latest tag
.. |Code Climate| image:: https://codeclimate.com/github/manga-py/manga-py/badges/gpa.svg
   :target: https://codeclimate.com/github/manga-py/manga-py
.. |Issue Count| image:: https://codeclimate.com/github/manga-py/manga-py/badges/issue_count.svg
   :target: https://codeclimate.com/github/manga-py/manga-py
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/manga-py.svg
   :target: https://pypi.org/project/manga-py/
.. |Scrutinizer CI result| image:: https://scrutinizer-ci.com/g/manga-py/manga-py/badges/quality-score.png?b=stable_1.x
   :target: https://scrutinizer-ci.com/g/manga-py/manga-py
.. |Scrutinizer CI coverage| image:: https://scrutinizer-ci.com/g/manga-py/manga-py/badges/coverage.png?b=stable_1.x
   :target: https://scrutinizer-ci.com/g/manga-py/manga-py
.. |GitHub issues| image:: https://img.shields.io/github/issues/manga-py/manga-py.svg
   :target: https://github.com/manga-py/manga-py/issues
.. |PyPi version| image:: https://badge.fury.io/py/manga-py.svg
   :alt: PyPI
   :target: https://pypi.org/project/manga-py/
.. |JetBrains logo| image:: https://github.com/yuru-yuri/manga-py/raw/stable_1.x/.github/jetbrains.png
   :alt: JetBrains
   :target: https://www.jetbrains.com/?from=manga-py
.. |MicroBadger Layers| image:: https://img.shields.io/microbadger/layers/mangadl/manga-py
   :alt: MicroBadger Layers
.. |MicroBadger Size| image:: https://img.shields.io/microbadger/image-size/mangadl/manga-py
   :alt: MicroBadger Size
.. |GitHub repo size| image:: https://img.shields.io/github/repo-size/manga-py/manga-py
   :alt: GitHub repo size
.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/manga-py
   :alt: PyPI - Downloads
.. |PyPI - size| image:: https://img.shields.io/badge/dynamic/json?label=PyPI%20size&query=%24.size&url=https%3A%2F%2Fpip.sttv.me%2Fmanga-py.json%3Fhuman-size%3Dtrue%26index%3D0%26version%3D1.29.5
   :alt: PyPI - size
