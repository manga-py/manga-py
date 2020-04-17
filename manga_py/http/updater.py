import json
import webbrowser

from packaging import version
from requests import get

from manga_py.meta import _version, _repo_name


def check_version():
    api_url = 'https://api.github.com/repos/' + _repo_name + '/releases/latest'
    api_content = json.loads(get(api_url).text)
    tag_name = api_content.get('tag_name', None)
    if tag_name and _version.parse(tag_name) > _version.parse(_version):
        download_addr = api_content['assets'][0]
        return tag_name, download_addr['browser_download_url']
    return ()


def download_update():
    pass


def open_browser(url):
    webbrowser.open(url)
