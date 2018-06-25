from threading import Thread


class MultiThreads:
    threads = None
    max_threads = 2
    to_run = None

    def __init__(self):
        self.threads = []
        self.to_run = []
        try:
            import multiprocessing
            self.max_threads = multiprocessing.cpu_count()
        except Exception:
            pass

    def add(self, target: callable, args: tuple):
        self.threads.append(Thread(target=target, args=args))

    def _run_processes(self, callback: callable = None, n: int = None):
        for t in self.to_run:
            if not n:
                t.join()
                callback is not None and callback()

    def start(self, callback: callable = None):
        for n, t in enumerate(self.threads):  # starting all threads
            t.start()
            self.to_run.append(t)
            self._run_processes(callback, (n + 1) % self.max_threads)
        self._run_processes(callback)
        self.threads = []
