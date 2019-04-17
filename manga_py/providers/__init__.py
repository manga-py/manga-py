from re import match

from typing import List
from .__list import providers_list
import importlib
from copy import deepcopy


__cache = {
    'providers': deepcopy(providers_list)
}


def add_providers(providers: List[dict]):
    __cache['providers'] += providers


def _sort(providers: List[dict]) -> list:
    def _(x: dict): return x.get('priority', 5)
    return sorted(providers, key=_, reverse=True)


def get_provider(url: str):
    for provider in _sort(__cache['providers']):
        for template in provider['templates']:
            if match(template, url) is not None:
                module = importlib.import_module(provider['provider'])
                return module.main
