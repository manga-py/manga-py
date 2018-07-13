from abc import abstractmethod


class Abstract:
    @abstractmethod
    def get_content(self):  # mixed
        """
        Returns mixed data on the main page.
        Used in methods get_manga_name, get_chapters, get_cover, book_meta
        Ideally, the main page is requested only once.
        (Use self.content to get data from the provider)

        Must correct the address of the main page if the user did not pass it correctly.
        (For example, instead of the address of the main page of the manga,
         the address of one of the chapters was given.
         Call self.url = 'http://example.org/manga/here' for this)
        :return:
        """
        pass

    @abstractmethod
    def get_manga_name(self) -> str:
        """
        Returns the name of the manga.
        Ideally, it is called only once. (Use self.manga_name to get data from the provider)
        :return:
        """
        pass

    @abstractmethod
    def get_chapters(self) -> list:
        """
        Returns the list of chapters.
        Ideally, it is called only once. (Use self.chapters to get data from the provider)

        The method is required to return a list of the form:
        [etree.Element, ...]
        or
        [('absolute_url', ('archive_name', 'folder_name')), ...]
        or
        [('absolute_url', ('archive_name', 'folder_name')), etree.Element, ...]

        The latter is not recommended, but can be used.
        :return:
        """
        pass

    @abstractmethod
    def get_files(self) -> list:
        """
        The method is required to return a list of the form:
        [etree.Element, ...]
        or
        [('absolute_url', 'relative_file_name'), ...]
        or
        [('absolute_url', 'relative_file_name'), etree.Element, ...]

        The latter is not recommended, but can be used.
        :return:
        """
        pass

    @abstractmethod
    def get_chapter_name(self) -> tuple:  # (archive_name_without_extension, folder_name)
        """
        Returns the current name of the chapter.
        It is called at each iteration of the chapter list. (Use self.chapter to get RAW data from the provider)
        :return:
        """
        pass

    def get_chapter_url(self) -> str:
        """
        Used to overload the standard behavior.
        Returns the current url of the chapter.
        It is called at each iteration of the chapter list. (Use self.chapter to get RAW data from the provider)
        :return:
        """
        pass

    def get_cover(self):
        """
        :return:
        """
        pass

    def prepare_cookies(self):
        """
        :return:
        """
        pass

    def book_meta(self):  # Todo
        """
        :return:
        """
        pass
