Security
========

Web applications face many kinds of security problems.
It's very hard to get everything right.
The manga-py project works with some security issues.
These are listed below.

Authentication (login with username/password)
---------------------------------------------

By default, manga-py does not input login by username/password to extract mangas from providers.
By *provider* means the manga-py source-code to extract mangas from one (specific) site.
The list of providers stay [here](https://github.com/manga-py/manga-py/tree/stable_1.x/manga_py/providers).
E.g.: manga-py uses one provider for `mangadex`_, another for `kissmanga`_, and so on.
So, about to use a default username/password, manga-py works like a guest user.

Providers login policy 
+++++++++++++++++++++++

Pay attention because each provider has its own policy.
It can be in these ways listed below.

Provider *does not requires* username/password
______________________________________________

The provider *does not requires* an username/password to show you the manga requested.
So manga-py can download without your input about your username and password data.
E.g.: `mangadex`_ or, `kissmanga`_ etc.
An usual input/output can be like below, without typing any username and password.

.. code:: bash

    $ manga-py https://mangadex.org/title/7249/cha-chu-cho
    /home/user/.local/lib/python3.6/site-packages/requests/__init__.py:91: RequestsDependencyWarning: urllib3 (1.25.2) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    Available languages:
    pl	--- Polish
    gb	--- English
    
    Please, select your lang (empty for all, space for delimiter lang):
    gb
    100% (10 of 10) |########################################################################################| Elapsed Time: 0:00:06 Time:  0:00:06
     
Provider *requires* username/password
_____________________________________

The provider *requires* an username/password to show you the manga requested.
So manga-py only will download with your input about your username and password data.
Pay attention: the same provider can *or* can not request your username/password to give the manga.
E.g.: `exhentai`_, `tapas`_ etc.
A case that requires the username and password:

.. code:: bash
    
    $ manga-py https://exhentai.org/g/1403504/ff38b6352a/
    /home/user/.local/lib/python3.6/site-packages/requests/__init__.py:91: RequestsDependencyWarning: urllib3 (1.25.2) or chardet (3.0.4) doesn't match a supported version!
      RequestsDependencyWarning)
    Request login on e-hentai.org
    my_fake_username    
    Request password on e-hentai.org
    
    Wrong password?
    
DDOS 
----

Avoid to download a lot of manga chapters in a short time.
Because you can get be banned from any manga's server.
The reason is: `DDOS`_ attack.
The server will detect that your IP is concentrating a lot of traffic.
And it thinks that can be a cracker (i.e. a bad person/software) to cause a DDOS attack.
So, to resolve that is simple: **be a nice user**, doing:

- download manga chapter *slowing*, wait some minutes between sent requests.
- if the server blocked you, wait days to retry download, or use another IP.
- if you are using manga-py programmatically (i.e. in a script, software, embedded), apply the best practices of crawling/scraping.

Protection by Cloudflare
++++++++++++++++++++++++

Some manga site uses Cloudflare system to be protected against DDOS attacks.
For sites with cloudflare protection, it is needed to install `Node.js`.
Examples of site that uses Cloudflare technology: `kissmanga`_, `mangahasu`_, etc.

Security issues
---------------

The project disclose all security vulnerabilities found, or that are advised about.
It can be published like a opened issue, a changelog, a commit message or, a pull request.
If you found a security issue, please use `GitHub Issues`_.

Issues with personal data
+++++++++++++++++++++++++

If you have security issues with personal/private data, please, do not publish your question on `GitHub Issues`_.
Because it will stay public.
Instead of, ask for help to one manga-py maintainer directly (i.e. private message), by:

- .. todo [EMAIL]
- .. todo [DISCORD]
- .. todo [ANY PRIVATE MESSAGE]

Besides that, avoid:

- *do not* send your username/password (GitHub, manga sites etc) to any maintainer.
- *do not* send files that was not asked for.

It can be applied if you are ashamed by your issue contains erotic manga reference.
And you do not want to be exposed to publish it publicly on `GitHub Issues`_.

.. _`mangadex`: https://mangadex.org/
.. _`kissmanga`: https://kissmanga.com/
.. _`mangahasu`: https://mangahasu.se/
.. _`exhentai`: https://exhentai.org/
.. _`tapas`: https://tapas.io/
.. _`DDOS`: https://en.wikipedia.org/wiki/Denial-of-service_attack
.. _`GitHub Issues`: https://github.com/manga-py/manga-py/issues
