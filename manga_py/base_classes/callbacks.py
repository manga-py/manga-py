from typing import Callable


class Callbacks:
    def _call_files_progress_callback(self):
        if callable(self.chapter_progress):
            _max, _current = len(self._storage['files']), self._storage['current_file']
            self.chapter_progress(_max, _current, _current < 1)

    def set_quest_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'quest', callback)

    def set_chapter_progress_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'chapter_progress', callback)

    def set_global_progress_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'global_progress', callback)

    def set_log_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'log', callback)

    def set_quest_password_callback(self, callback: Callable):  # Required call from iterator (CLI, GUI)
        setattr(self, 'quest_password', callback)

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
