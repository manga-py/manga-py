
class Manga:
    __storage = None

    def __init__(self, **kwargs):
        self.__storage = kwargs

    def get_data(self) -> dict:
        return self.__storage.copy()

    @property
    def authors(self) -> list:
        """
        one or more
        :return:
        """
        return self.__storage['authors']

    @authors.setter
    def authors(self, authors: list):
        self.__storage['authors'] = authors

    @property
    def year(self) -> int:
        return self.__storage['year']

    @year.setter
    def year(self, year: int):
        self.__storage['year'] = year

    @property
    def description(self) -> str:
        return self.__storage['description']

    @description.setter
    def description(self, description: str):
        self.__storage['description'] = description

    @property
    def rating(self) -> float:
        """
        always x out of 10
        :return:
        """
        return self.__storage['rating']

    @rating.setter
    def rating(self, rating: float):
        self.__storage['rating'] = rating

    @property
    def title(self) -> str:
        """
        original title
        :return:
        """
        return self.__storage['title']

    @title.setter
    def title(self, title: str):
        self.__storage['title'] = title
