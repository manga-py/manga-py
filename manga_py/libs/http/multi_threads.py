from threading import Thread

# see: https://python-scripts.com/threading


class MultiThreads:
    threads = None
    max_threads = 2
    _to_run = None
    _current_threads = 0

    def __init__(self):
        self.threads = []
        self._to_run = []
        self._current_threads = 0
        try:
            import multiprocessing
            self.max_threads = min(multiprocessing.cpu_count(), 8) / 2
            if self.max_threads < 2:
                self.max_threads = 2
        except ImportError:
            self.max_threads = 2

    def add(self, target: callable, args: tuple):
        self.threads.append(Thread(target=target, args=args))

    def _run_processes(self, callback: callable = None, n: int = 0):
        if n > 0:
            return
        for t in self._to_run:
            t.join()
            callback is not None and callback()

    def start(self, callback: callable = None):
        for n, t in enumerate(self.threads):  # starting all threads
            t.start()
            self._to_run.append(t)
            self._run_processes(callback, (n + 1) % self.max_threads)
        self._run_processes(callback)
        self.threads = []
