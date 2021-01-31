from typing import Callable


class Callbacks:
    def _set_default_if_not_callable(self, attr_name: str, callback: Callable, default: Callable):
        cb = callback if callable(callback) else default
        setattr(self, attr_name, cb)

    def set_quest_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        self._set_default_if_not_callable('quest', callback, self.quest)

    def set_chapter_progress_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        self._set_default_if_not_callable('chapter_progress', callback, self.progress)

    def set_global_progress_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        self._set_default_if_not_callable('global_progress', callback, self.progress)

    def set_log_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
         self._set_default_if_not_callable('log', callback, self.progress)

    def set_quest_password_callback(self, callback: Callable):  # Required call from iterator (CLI, GUI)
        self._set_default_if_not_callable('quest_password', callback, self.progress)

    def quest(self, *args, **kwargs):
        pass

    def quest_password(self, *args, **kwargs):
        pass

    def progress(self, *args, **kwargs):
        pass

    def log(self, *args, **kwargs):
        pass

    def book_meta(self) -> dict:
        return {}
