from re import match

from typing import List
from .__list import providers_list


__cache = {
    'providers': providers_list[:]
}


def add_providers(providers: List[dict]):
    __cache['providers'] += providers


def get_provider(url: str):
    for provider in sort(providers_list):
        for template in provider['templates']:
            if match(template, url) is not None:
                return provider['provider']


def sort(providers: List[dict]) -> list:
    def _sort(x: dict):
        return x.get('priority', 5)
    return sorted(providers, key=_sort, reverse=True)
