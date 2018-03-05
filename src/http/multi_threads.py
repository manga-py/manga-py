from threading import Thread


class MultiThreads:
    threads = None
    max_threads = 2

    def __init__(self):
        self.threads = []
        try:
            import multiprocessing
            self.max_threads = multiprocessing.cpu_count()
        except Exception:
            pass

    def add(self, target: callable, args: tuple):
        self.threads.append(Thread(target=target, args=args))

    def _run_processes(self, to_run, callback: callable=None):
        for t in to_run:
            t.join()

    def start(self, callback: callable=None):
        to_run = []
        for n, t in enumerate(self.threads):  # starting all threads
            t.start()
            to_run.append(t)
            if n > 0 and n % self.max_threads == 0:
                self._run_processes(to_run, callback)
                to_run = []
        if len(to_run):
            self._run_processes(to_run, callback)
        self.threads = []
