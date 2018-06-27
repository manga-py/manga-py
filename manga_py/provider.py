from abc import ABCMeta

from .libs.base import Base


class Provider(Base, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    def run(self, params: dict):
        pass
