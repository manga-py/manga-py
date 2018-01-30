from setuptools import setup
from libs.version import __version__

github = 'https://github.com/yuru-yuri/manga-dl'

setup(
    name='manga_dl',
    packages=['manga_dl'],
    include_package_data=True,
    version=__version__,
    description='Universal assistant download manga.',
    author='Zharkov Sergey',
    author_email='sttv-pc@mail.ru',
    url=github,
    download_url='{}/manga-dl/archive/{}.tar.gz'.format(github, __version__),
    keywords=['manga-downloader', 'manga', 'automatically'],
    license='MIT',
    classifiers=[  # look here https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        'lxml>=3.7.2',
        'cssselect>=1.0.0',
        'requests>=2.14',
        'pycrypto>=2.5',
        'cfscrape>=1.9.1',
        'tldextract>2.1',
    ],
)
