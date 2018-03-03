from typing import Callable


class Callbacks:
    def _call_files_progress_callback(self):
        if callable(self.progress):
            _max, _current = len(self._storage['files']), self._storage['current_file']
            self.progress(_max, _current, _current < 1)

    def set_quest_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'quest', callback)

    def set_progress_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'progress', callback)

    def set_log_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'log', callback)

    def quest(self, *args, **kwargs):
        pass

    def progress(self, *args, **kwargs):
        pass

    def log(self, *args, **kwargs):
        pass
