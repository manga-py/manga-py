from argparse import ArgumentParser
from typing import Optional, List


class ArgsListHelper:
    __slots__ = ('__store',)
    __doc__ = """
    helper-class for the argument list
    """

    def __init__(self, args: ArgumentParser):
        self.__store = args

    def as_dict(self):
        return self.__store.__dict__

    def get(self, name, default=None):
        if isinstance(name, str):
            name = name.replace('-', '_')

        return getattr(self.__store, name=name, default=default)

    # general
    @property
    def url(self) -> List[str]:
        return self.__store.url

    @property
    def title(self) -> Optional[str]:
        return self.__store.title

    @property
    def name(self) -> Optional[str]:
        return self.__store.name

    @property
    def destination(self) -> Optional[str]:
        return self.__store.destination

    @property
    def print_json(self) -> bool:
        return self.__store.print_json

    @property
    def simulate(self) -> bool:
        return self.__store.simulate

    @property
    def show_log(self) -> bool:
        return self.__store.show_log

    @property
    def no_progress(self) -> bool:
        return self.__store.no_progress

    @property
    def force_make_db(self) -> bool:
        return self.__store.force_make_db

    @property
    def do_not_use_database(self) -> bool:
        return self.__store.do_not_use_database

    @property
    def do_not_clear_temporary_directory(self) -> bool:
        return self.__store.do_not_clear_temporary_directory

    # downloading
    @property
    def not_change_files_extension(self) -> bool:
        return self.__store.not_change_files_extension

    @property
    def update_all(self) -> bool:
        return self.__store.update_all

    @property
    def skip_volumes(self) -> Optional[int]:
        return self.__store.skip_volumes

    @property
    def max_volumes(self) -> Optional[int]:
        return self.__store.max_volumes

    @property
    def user_agent(self) -> Optional[str]:
        return self.__store.user_agent

    @property
    def reverse_downloading(self) -> bool:
        return self.__store.reverse_downloading

    @property
    def rewrite_exists_archives(self) -> bool:
        return self.__store.rewrite_exists_archives

    @property
    def no_multi_threads(self) -> bool:
        return self.__store.no_multi_threads

    @property
    def zero_fill(self) -> bool:
        return self.__store.zero_fill

    @property
    def min_free_space(self) -> Optional[int]:
        return self.__store.min_free_space

    @property
    def with_website_name(self) -> bool:
        return self.__store.with_website_name

    # image
    @property
    def png(self) -> bool:
        return self.__store.png

    @property
    def jpg(self) -> bool:
        return self.__store.jpg

    @property
    def grayscale(self) -> bool:
        return self.__store.grayscale

    @property
    def Xt(self) -> Optional[int]:
        return self.__store.Xt

    @property
    def Xr(self) -> Optional[int]:
        return self.__store.Xr

    @property
    def Xb(self) -> Optional[int]:
        return self.__store.Xb

    @property
    def Xl(self) -> Optional[int]:
        return self.__store.Xl

    @property
    def crop_blank(self) -> bool:
        return self.__store.crop_blank

    @property
    def split_images(self) -> bool:
        return self.__store.split_images

    # reader
    @property
    def cbz(self) -> bool:
        return self.__store.cbz

    @property
    def zip(self) -> bool:
        return self.__store.zip

    @property
    def rename_pages(self) -> bool:
        return self.__store.rename_pages

    @property
    def html(self) -> bool:
        return self.__store.html
