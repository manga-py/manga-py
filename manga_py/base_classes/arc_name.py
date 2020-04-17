from abc import abstractmethod, ABCMeta


class ArchiveName(metaclass=ABCMeta):
    _vol_fill = False

    @abstractmethod
    def get_chapter_index(self):
        pass

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        self._vol_fill = True
        return self.normal_arc_name({'vol': idx.split('-')})

    def normal_arc_name(self, idx):
        if isinstance(idx, str):
            idx = [idx]
        if isinstance(idx, list):
            self._vol_fill = True
            return self.__normal_name_list(idx)
        if isinstance(idx, dict):
            return self.__normal_name_dict(idx)
        raise DeprecationWarning('Wrong arc name type: %s' % type(idx))

    def __normal_name_dict(self, idx: dict):
        vol = idx.get('vol', None)
        ch = idx.get('ch', None)
        result = ''
        if vol:
            if isinstance(vol, str):
                vol = [vol]
            result = self.__normal_name_list(vol)
        if ch:
            result += '-ch_' + self.__fill(ch)

        if self._with_manga_name:
            name = self._params.get('name', '')
            if not len(name):
                name = self.manga_name

            result = '%s-%s' % (name, result)

        return result

    def __normal_name_list(self, idx: list):
        fmt = 'vol_{:0>3}'
        if len(idx) > 1:
            fmt += '-{}' * (len(idx) - 1)
        elif self._vol_fill and self._zero_fill:
            idx.append('0')
            fmt += '-{}'
        return fmt.format(*idx)

    @staticmethod
    def __fill(var, fmt: str = '-{}'):
        if isinstance(var, str):
            var = [var]
        return (fmt * len(var)).format(*var).lstrip('-')
